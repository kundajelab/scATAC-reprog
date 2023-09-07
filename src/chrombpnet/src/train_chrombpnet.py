import keras
import archs
from utils import data_utils, train_utils, augment, argmanager
from utils.loss import multinomial_nll
import numpy as np
import random
import string
import math
import os
import json


class ChromBPNetBatchGenerator(keras.utils.Sequence):
    """
    This generator randomly crops (=jitter) and revcomps training examples for 
    every epoch, and calls bias model on it, whose outputs (bias profile logits 
    and bias logcounts) are fed as input to the chrombpnet model.
    """
    def __init__(self, model_bias, seqs, cts, seqlen, batch_size):
        """
        model_bias: model that predicts bias logits and logcounts, input and output
                    size L (seqlen)
        seqs: B x L' x 4
        cts: B x L'
        seqlen: int (L <= L'), L' is greater to allow for cropping (= jittering)
        batch_size: int (B)
        """

        self.model_bias = model_bias
        self.seqs = seqs
        self.cts = cts
        self.seqlen = seqlen
        self.batch_size = batch_size

        # random crop training data to seqlen, revcomp augmentation
        self.crop_revcomp_data()

    def __len__(self):
        return math.ceil(self.seqs.shape[0]/self.batch_size)

    def crop_revcomp_data(self):
        # random crop training data to seqlen, revcomp augmentation
        # shuffle required since otherwise peaks and nonpeaks will be together
        self.cur_seqs, self.cur_cts = augment.crop_revcomp_augment(
                                         self.seqs, self.cts, self.seqlen, 
                                         shuffle=True
                                      )


        # apply bias model to those     
        self.cur_bias_logits, self.cur_bias_logcts = self.model_bias.predict(self.cur_seqs)

    def __getitem__(self, idx):
        batch_seq = self.cur_seqs[idx*self.batch_size:(idx+1)*self.batch_size]
        batch_cts = self.cur_cts[idx*self.batch_size:(idx+1)*self.batch_size]
        
        batch_bias_logits = self.cur_bias_logits[idx*self.batch_size:(idx+1)*self.batch_size]
        batch_bias_logcts = self.cur_bias_logcts[idx*self.batch_size:(idx+1)*self.batch_size]

        return [batch_seq, batch_bias_logits, batch_bias_logcts], [batch_cts, np.log(1+batch_cts.sum(-1, keepdims=True))] 

    def on_epoch_end(self):
        self.crop_revcomp_data()


def train_loop(model_chrombpnet, model_bias, seqlen, train_seqs, train_cts, 
               val_seqs, val_cts, batch_size, epochs, early_stop, output_dir, 
               expt_tag):

    # need generator to crop and revcomp aug training examples, but not for 
    # validation. Also applies bias model to cropped, rev comp-ed seqs.
    train_generator = ChromBPNetBatchGenerator(model_bias, train_seqs, 
                                               train_cts, seqlen, batch_size)

    # predict validation bias logits and logcounts
    val_bias_logits, val_bias_logcts = model_bias.predict(val_seqs)

    callbacks = train_utils.get_callbacks(early_stop, output_dir, expt_tag)

    history = model_chrombpnet.fit_generator(train_generator, 
                        epochs=epochs,
                        validation_data=[[val_seqs, val_bias_logits, val_bias_logcts],
                                         [val_cts, 
                                          np.log(1+val_cts.sum(-1, keepdims=True))]],
                        callbacks=callbacks)

    return history


def adjust_bias_model_logcounts(bias_model, seqs, cts):
    """
    Given a bias model, sequences and associated counts, the function adds a 
    constant to the output of the bias_model's logcounts that minimises squared
    error between predicted logcounts and observed logcounts (infered from 
    cts). This simply reduces to adding the average difference between observed 
    and predicted to the "bias" (constant additive term) of the Dense layer.

    Typically the seqs and counts would correspond to training nonpeak regions.

    ASSUMES model_bias's last layer is a dense layer that outputs logcounts. 
    This would change if you change the model.
    """
    
    # safeguards to prevent misuse
    assert(bias_model.layers[-1].name == "logcounts")
    assert(bias_model.layers[-1].output_shape==(None,1))
    assert(isinstance(bias_model.layers[-1], keras.layers.Dense))

    print("Predicting within adjust counts")
    _, pred_logcts = bias_model.predict(seqs, verbose=True)
    
    delta = np.mean(np.log(1+cts.sum(-1)) - pred_logcts.ravel())

    dw, db = bias_model.layers[-1].get_weights()
    bias_model.layers[-1].set_weights([dw, db+delta])

    return bias_model


def main():
    args = argmanager.fetch_train_chrombpnet_args()
    print(args)

    expt_tag = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    # load bias model
    with keras.utils.CustomObjectScope({'multinomial_nll':multinomial_nll}):
        model_bias = keras.models.load_model(args.bias_model)

    # input and output shapes to bias model should be same as seqlen, 
    # which are input and output lengths for chrombpnet model
    assert(model_bias.input_shape[1]==args.seqlen)
    assert(model_bias.output_shape[0][1]==args.seqlen)

    # load data
    train_peaks_seqs, train_peaks_cts, train_nonpeaks_seqs, train_nonpeaks_cts,\
    val_peaks_seqs, val_peaks_cts, val_nonpeaks_seqs, val_nonpeaks_cts =  \
                            data_utils.load_train_val_data(
                                args.peaks, args.nonpeaks, args.genome, args.bigwig,
                                args.val_chr, args.test_chr, args.seqlen, args.max_jitter,
                                outlier=0.9999
                            )

    # adjust bias model predicted counts to accounts for sequencing depth of 
    # current sample. The adjustment is done on nonpeak regions. Note that this
    # will slightly update even if the bias model is trained on the current 
    # sample, since during training bias model, the nonpeaks regions used for
    # training are those below a stringent threshold
    if args.adjust_bias_cts:
        # crop seqlen from center of nonpeaks
        slice_start = train_nonpeaks_seqs.shape[1]//2 - args.seqlen//2
        slice_end = train_nonpeaks_seqs.shape[1]//2 + args.seqlen//2
        model_bias = adjust_bias_model_logcounts(model_bias, 
                                    train_nonpeaks_seqs[:, slice_start:slice_end], 
                                    train_nonpeaks_cts[:, slice_start:slice_end])

        # save adjusted bias model
        model_bias.save(os.path.join(args.output_dir, 
                               "{}.adjusted_bias_model.h5".format(expt_tag)))

    # compute loss weight factor for counts loss
    counts_loss_weight = train_utils.get_counts_stat(
                          np.vstack([train_peaks_cts, train_nonpeaks_cts]), 
                                     args.seqlen) * args.counts_weight
    print("\nCounts loss weight : {:.2f}\n".format(counts_loss_weight))

    # prepare chrombpnet model
    model_chrombpnet = archs.chrombpnet(args.seqlen, args.filters, args.ndil) 
    opt = keras.optimizers.Adam(lr=args.learning_rate)
    model_chrombpnet.compile(
            optimizer=opt,
            loss=[multinomial_nll, 'mse'],
            loss_weights = [1, counts_loss_weight]
        )

    history = train_loop(model_chrombpnet, model_bias, args.seqlen, 
                         np.vstack([train_peaks_seqs, train_nonpeaks_seqs]),
                         np.vstack([train_peaks_cts, train_nonpeaks_cts]),
                         np.vstack([val_peaks_seqs, val_nonpeaks_seqs]),
                         np.vstack([val_peaks_cts, val_nonpeaks_cts]),
                         args.batch_size, args.epochs, 
                         args.early_stop, args.output_dir, expt_tag)

    with open(os.path.join(args.output_dir, "{}.history.json".format(expt_tag)), "w") as f: 
        json.dump(history.history, f, ensure_ascii=False, indent=4)

if __name__=="__main__":
    main()

