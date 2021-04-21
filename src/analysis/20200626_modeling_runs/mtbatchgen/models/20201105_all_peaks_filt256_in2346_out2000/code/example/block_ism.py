import argparsers
import time
import datetime
import json
import os
import pandas as pd
import sys

import logger
import bigwigutils
import MTBatchGenerator

from batchgenutils import *
from utils import *
from losses import MultichannelMultinomialNLL, multinomial_nll

from keras.models import load_model
from keras.utils import CustomObjectScope
from tqdm import tqdm

def predict(args, input_data, pred_dir):    
    # load the model
    model = load_model(args.model)

    # parameters that are specific to the batch generation process.
    # for prediction we dont use jitter, reverse complement 
    # augmentation and negative sampling
    batchgen_params = {'seq_len': args.input_seq_len,
                       'output_len': args.output_len,
                       'jitter': 0, 
                       'rev_comp_aug': False,
                       'negative_sampling_rate': 0.0}
    
    pred_ism_intervals = pd.read_csv(args.bed_file, sep='\t', header=None, 
                                     names=['chrom', 'st', 'end'])
    pred_ism_intervals['pos'] = (pred_ism_intervals['st'] + pred_ism_intervals['end'])//2
    orig_num_examples = len(pred_ism_intervals.index)
    
    if args.batch_size > 1:
        repeat_last_times = (args.batch_size - (len(pred_ism_intervals.index) % args.batch_size)) % args.batch_size
        pred_ism_intervals=  pred_ism_intervals.append(pred_ism_intervals.iloc[[-1]*repeat_last_times])

         
    test_data = pred_ism_intervals[['chrom', 'pos']]                
    
    logging.info("Test data size {}".format(test_data.shape))

    # instantiate the batch generator class for testing
    BatchGenerator = getattr(MTBatchGenerator, 
                             'MT{}BatchGenerator'.format(args.model_name))
    test_gen = BatchGenerator(input_data, args.reference_genome, 
                              args.chrom_sizes, 
                              list(test_data['chrom'].unique()), # chromosomes
                              batchgen_params, 
                              "test_gen", num_threads=1, epochs=1, 
                              batch_size=args.batch_size, shuffle=False,
                              mode='test')

    # testing generator function
    test_generator = test_gen.gen(test_data)
         
    # begin time for training
    t1 = time.time()
              
    # extract the basename from the model filename and 
    # remove the extension
    model_tag = os.path.basename(args.model).split('.')[0]
    
    # total number of batches that will be generated
    num_batches = test_data.shape[0] // args.batch_size

    # list of batch outputs, each batch will have interleaved reference/mut 
    # predicted outputs for all tasks
    all_ref_mut_interleaved_predictions = []    

    # run predict on each batch separately
    cnt_batches = 0
    for coordinates, batch in tqdm(
        test_generator, desc='batch', total=num_batches):

        # predict on reference
        predictions_ref = model.predict(batch)
        
        # set centers to 0 (control left unchanged)
        for i in range(args.batch_size):
            cur_interval = pred_ism_intervals.iloc[cnt_batches*args.batch_size+i]
            cur_start = (args.input_seq_len - (cur_interval['end']-cur_interval['st']))//2
            cur_end = cur_start + cur_interval['end']-cur_interval['st']
             
            # add 1bp on both sides
            cur_start, cur_end = cur_start-1, cur_end+1

            batch['sequence'][i][cur_start:cur_end] = 0

        predictions_mut = model.predict(batch)

        # write to file
        # interleave predicted ref/mut counts
        ref_mut_interleaved = np.zeros((predictions_ref[1].shape[0], predictions_ref[1].shape[1]*2))
        ref_mut_interleaved[:, 0::2] = predictions_ref[1] 
        ref_mut_interleaved[:, 1::2] = predictions_mut[1]
        all_ref_mut_interleaved_predictions.append(ref_mut_interleaved)
     
        cnt_batches += 1

        if cnt_batches == num_batches:
            break

    # gracefully terminate when prediction on all batches is complete
    # send the stop signal to the generators
    test_gen.set_stop()
     
    # write reference and mutation predicted counts will be written
    all_ref_mut_interleaved_predictions = np.vstack(all_ref_mut_interleaved_predictions)

    outfile = open(os.path.join(pred_dir, "predicted.counts.tsv"), 'w')
    outfile.write("chr\tstart\tend")
    
    for i in range(len(input_data)):
        outfile.write("\tref_task_{}\tmut_task_{}".format(i,i))
    outfile.write("\n")

    for i in range(orig_num_examples):
        cur_interval = pred_ism_intervals.iloc[i][['chrom','st','end']]
        outfile.write("\t".join([str(x) for x in cur_interval.to_list() + list(all_ref_mut_interleaved_predictions[i])]) + "\n")
    
    outfile.close()

    # end time for training
    t2 = time.time() 
    logging.info('Total Elapsed Time: {} secs'.format(t2-t1))

    # write all the command line arguments to a json file
    config_file = '{}/config.json'.format(pred_dir)
    with open(config_file, 'w') as fp:
        json.dump(vars(args), fp)
        
def predict_main():
    # parse the command line arguments
    parser = argparsers.block_ism_argsparser()
    args = parser.parse_args()

    # check if the output directory exists
    if not os.path.exists(args.output_dir):
        logging.error("Directory {} does not exist".format(
            args.output_dir))
        
        return

    if args.automate_filenames:
        # create a new directory using current date/time to store the
        # predictions and logs
        date_time_str = local_datetime_str(args.time_zone)
        pred_dir = '{}/{}'.format(args.output_dir, date_time_str)
        os.mkdir(pred_dir)
    elif os.path.isdir(args.output_dir):
        pred_dir = args.output_dir        
    else:
        logging.error("Directory does not exist {}.".format(args.output_dir))
        return

    # filename to write debug logs
    logfname = "{}/predict.log".format(pred_dir)
    
    # set up the loggers
    logger.init_logger(logfname)
    
    # get the dictionary of input tasks
    input_data = getInputTasks(args.data_dir, stranded=args.stranded, 
                               has_control=args.has_control, mode='test',
                               require_peaks=False)

    # if there was a problem constructing the input tasks dictionary
    if input_data is None:
        return

    if len(input_data) == 0:
        logging.error("The --data-dir supplied does not seem to have the "
                      "correct data. Please correct your path and try again.")
        return
        
    logging.info("INPUT DATA -\n{}".format(input_data))

    # predict
    logging.info("Loading {}".format(args.model))
    with CustomObjectScope({'MultichannelMultinomialNLL': 
                            MultichannelMultinomialNLL}):
            
        predict(args, input_data, pred_dir)
    
if __name__ == '__main__':
    predict_main()
