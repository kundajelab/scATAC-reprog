from keras.callbacks import ModelCheckpoint, EarlyStopping
import numpy as np
import os


def get_callbacks(early_stop, output_dir, expt_tag):
    early_stop_callback = EarlyStopping(monitor='val_loss',
                                        patience=early_stop,
                                        verbose=1,
                                        mode='min')

    filepath = os.path.join(output_dir,"{}.h5".format(expt_tag))
    checkpoint_callback = ModelCheckpoint(filepath,
                                          monitor='val_loss',
                                          verbose=1,
                                          save_best_only=True,
                                          mode='min')

    return [early_stop_callback, checkpoint_callback]

def get_counts_stat(cts, seqlen):
    """
    cts: N x L'
    seqlen: int L <= L'

    Compute mean reads per example in central seqlen
    """
    slice_start = cts.shape[1]//2 - seqlen//2
    slice_end = cts.shape[1]//2 + seqlen//2

    return np.mean(cts[:, slice_start:slice_end].sum(-1))
