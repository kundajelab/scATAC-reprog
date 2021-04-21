import argparse

def training_argsparser():
    # command line arguments
    parser = argparse.ArgumentParser()
    
    # training params
    parser.add_argument('--batch-size', '-b', type=int, 
                        help="training batch size", default=64)
    
    parser.add_argument('--epochs', '-e', type=int,
                        help="number of training epochs", default=100)

    parser.add_argument('--learning-rate', '-L', type=float,
                        help="learning rate for Adam optimizer",
                        default=0.004)

    parser.add_argument('--min-learning-rate', '-l', type=float,
                        help="min learning rate for Adam optimizer",
                        default=0.0001)
    
    parser.add_argument('--early-stopping-patience', type=int, 
                        help="patience value for early stopping callback", 
                        default=5)
    
    parser.add_argument('--early-stopping-min-delta', type=float, 
                        help="minimum change in the validation loss to "
                        "qualify as an improvement", default=1e-3)

    parser.add_argument('--reduce_lr_on_plateau-patience', type=int, 
                        help="patience value for ReduceLROnPlateau callback", 
                        default=2)

    # training modes
    parser.add_argument('--train-peaks', action='store_true', 
                        help="train on peaks contained in the peaks.bed files")
    
    parser.add_argument('--train-intervals', nargs='+', type=int,
                        help="train on positions at equal intervals, "
                        "specify two values <num_positions> <step>. If "
                        "num_positions is -1 then positions across the "
                        "entire chromosome are used (superceded by "
                        "--train-peaks)", default=[-1, 200])

    parser.add_argument('--train-random', type=int, 
                        help="train on randomly sampled positions on the "
                        "chromosomes. Specify an int value <num_positions>. "
                        "num_positions has to be a positive number.", 
                        default = 10000)

    # model params
    # TODO - might want to yaml just the model params 
    # the arguments here are specific to BPNet
    parser.add_argument('--model-arch-name', type=str,
                        help="the name of the model architesture that will "
                        "be used in training (the name that will be used "
                        "to fetch the model from model_archs)",
                        default='BPNet')

    parser.add_argument('--filters', '-f', type=int,
                        help="number of filters to use in BPNet",
                        default=64)

    parser.add_argument('--counts-loss-weight', '-w', type=float,
                        help="Weight for counts mse loss",
                        default=100.0)
    
    # parallelization params
    parser.add_argument('--threads', '-t', type=int,
                        help="number of parallel threads for batch "
                        "generation", default=10)
        
    parser.add_argument('--gpus', '-p', type=int,
                        help="number of gpus to use", default=1)
    
    # reference params
    parser.add_argument('--reference-genome', '-g', type=str, required=True,
                        help="number of gpus to use", default=1)
    
    parser.add_argument('--chrom-sizes', '-c', type=str, required=True,
                        help="path to chromosome sizes file")
    
    # validation params
    parser.add_argument('--splits', '-s', type=str,
                        help="string name of the function from 'experiments' "
                        "that returns the validation and test splits to use", 
                        default='10_human_val_test_splits')

    # output params    
    parser.add_argument('--output-dir', '-d', type=str,
                        help="destination directory to store the model", 
                        default=".")
    
    parser.add_argument('--tag-length', type=int,
                        help="length of the alphanumeric tag for the model "
                        "file name (applies if --automate-filenames option "
                        "is used)", default=6)

    parser.add_argument('--time-zone', type=str,
                        help="time zone to use for timestamping model "
                        "directories (applies if --automate-filenames "
                        "option is used)", default='US/Pacific')

    parser.add_argument('--automate-filenames', action='store_true', 
                        help="specify if the model output directory "
                        "and filename should be auto generated")

    parser.add_argument('--other-tags', nargs='+',
                        help="list of additional tags to be added as "
                        "suffix to the filenames", default=[])
        
    parser.add_argument('--model-output-filename', type=str,
                        help="basename of the model file without the .h5 "
                        "extension (required if --automate-filenames is "
                        "not used)")

    # batch gen parameters
    parser.add_argument('--input-seq-len', type=int, 
                        help="length of input DNA sequence", default=1346)

    parser.add_argument('--output-len', type=int, 
                        help="length of output profile", default=1000)

    parser.add_argument('--max-jitter', type=int, 
                        help="maximum value for randomized jitter to offset "
                        "the peaks from the exact center of the input",
                        default=128)

    parser.add_argument('--reverse-complement-augmentation', 
                        action='store_true', 
                        help="enable reverse complement augmentation", 
                        default=True)
    
    parser.add_argument('--negative-sampling-rate', type=float,
                        help="number of negatives to sample for every "
                        "positive peak", default=0.0)
        
    # input data params
    parser.add_argument('--input-dir', '-i', type=str,
                        help="input directory containing bigWigs and peaks", 
                        default=".")
    
    parser.add_argument('--stranded', action='store_true', 
                        help="specify if the input data is stranded or "
                        "unstranded")

    parser.add_argument('--has-control', action='store_true', 
                        help="specify if the input data has controls")

    parser.add_argument('--chroms', nargs='+', required=True,
                        help="master list of chromosomes for the genome")
    
    parser.add_argument('--exclude-chroms', nargs='+', help="list of "
                        "chromosomes to be excluded", default=[])    
    
    return parser


def predict_argsparser():
    """ Command line arguments for the predict script

        Returns:
            argparse.ArgumentParser
    """
    
    parser = argparse.ArgumentParser()
    
    # batch gen parameters
    parser.add_argument('--batch-size', '-b', type=int, help="test batch size",
                        default=64)
        
    parser.add_argument('--input-seq-len', type=int, 
                        help="length of input DNA sequence", default=1346)

    parser.add_argument('--output-len', type=int, 
                        help="length of output profile", default=1000)
    
    # predict modes
    parser.add_argument('--predict-peaks', action='store_true', 
                        help="generate predictions only on the peaks "
                        "contained in the peaks.bed files")

    # reference params
    parser.add_argument('--reference-genome', '-g', type=str, required=True,
                        help="the path to the reference genome fasta file")
    
    parser.add_argument('--chrom-sizes', '-s', type=str, required=True,
                        help="path to chromosome sizes file")
    
    # input data params
    parser.add_argument('--chroms', '-c', nargs='+', required=True,
                        help="list of test chromosomes for prediction")
        
    parser.add_argument('--data-dir', type=str,
                        help="input directory containing bigWigs and peaks", 
                        default=".")
    
    parser.add_argument('--stranded', action='store_true', 
                        help="specify if the input data is stranded or "
                        "unstranded (i.e in case --has-control is True)")

    parser.add_argument('--has-control', action='store_true', 
                        help="specify if the input data has controls")
    
    parser.add_argument('--model', '-m', type=str, 
                        help="path to the .h5 model file")

    parser.add_argument('--model-name', type=str,
                        help="the name of the model that will be used in "
                        "for predictions", default='BPNet')
    
    parser.add_argument('--model-dir', type=str,
                        help="directory where .h5 model files are stored")
    
    # output params
    parser.add_argument('--output-dir', '-o', type=str, required=True,
                        help="destination directory to store predictions as a "
                        "bigWig file")

    parser.add_argument('--automate-filenames', action='store_true', 
                        help="specify if the predictions output should "
                        "be stored in a timestamped subdirectory within "
                        "--output-dir")
    
    parser.add_argument('--time-zone', type=str,
                        help="time zone to use for timestamping model "
                        "directories", default='US/Pacific')
    
    parser.add_argument('--exponentiate-counts', action='store_true', 
                        help="specify if the predicted counts should be "
                        "exponentiated before writing to the bigWig files")

    parser.add_argument('--output-window-size', type=int,
                        help="size of the central window of the output "
                        "profile predictions that will be written to the "
                        "bigWig files", default=1000)

    parser.add_argument('--other-tags', nargs='+',
                        help="list of additional tags to be added as "
                        "suffix to the filenames", default=[])

    # misc params
    parser.add_argument('--write-buffer-size', type=int,
                        help="size of the write buffer to store predictions "
                        "before writing to bigWig files", default=10000)
    return parser


def block_ism_argsparser():
    """ Command line arguments for the block_ism script

        Returns:
            argparse.ArgumentParser
    """
    
    parser = argparse.ArgumentParser()
    
    # batch gen parameters
    parser.add_argument('--batch-size', '-b', type=int, help="test batch size",
                        default=64)
        
    parser.add_argument('--input-seq-len', type=int, 
                        help="length of input DNA sequence", default=1346)

    parser.add_argument('--output-len', type=int, 
                        help="length of output profile", default=1000)
    
    # predict modes
    parser.add_argument('--bed-file', '-r', type=str, required=True,
                        help="the path to the bed file containing "
                        "intervals which should be zero-d out. The sequence"
                        "is centered around the interval")

    # reference params
    parser.add_argument('--reference-genome', '-g', type=str, required=True,
                        help="the path to the reference genome fasta file")
    
    parser.add_argument('--chrom-sizes', '-s', type=str, required=True,
                        help="path to chromosome sizes file")
    
        
    parser.add_argument('--data-dir', type=str,
                        help="input directory containing bigWigs and peaks", 
                        default=".")
    
    parser.add_argument('--stranded', action='store_true', 
                        help="specify if the input data is stranded or "
                        "unstranded (i.e in case --has-control is True)")

    parser.add_argument('--has-control', action='store_true', 
                        help="specify if the input data has controls")
    
    parser.add_argument('--model', '-m', type=str, 
                        help="path to the .h5 model file")

    parser.add_argument('--model-name', type=str,
                        help="the name of the model that will be used in "
                        "for predictions", default='BPNet')
    
    parser.add_argument('--model-dir', type=str,
                        help="directory where .h5 model files are stored")
    
    # output params
    parser.add_argument('--output-dir', '-o', type=str, required=True,
                        help="destination directory to store predictions as a "
                        "bigWig file")

    parser.add_argument('--automate-filenames', action='store_true', 
                        help="specify if the predictions output should "
                        "be stored in a timestamped subdirectory within "
                        "--output-dir")
    
    parser.add_argument('--time-zone', type=str,
                        help="time zone to use for timestamping model "
                        "directories", default='US/Pacific')
    
    parser.add_argument('--output-window-size', type=int,
                        help="size of the central window of the output "
                        "profile predictions that will be written to the "
                        "bigWig files", default=1000)

    parser.add_argument('--other-tags', nargs='+',
                        help="list of additional tags to be added as "
                        "suffix to the filenames", default=[])

    return parser


def metrics_argsparser():
    """ Command line arguments for the metrics script

        Returns:
            argparse.ArgumentParser
    """
    
    parser = argparse.ArgumentParser()
    
    # input params
    parser.add_argument('--profileA', '-A', type=str, required=True,
                        help="the bigWig with ground truth values or a "
                        "replicate")

    parser.add_argument('--profileB', '-B', type=str, required=True,
                        help="the bigWig with predicted values or the "
                        "second replicate")

    parser.add_argument('--smooth-profileA', nargs='+',
                        help="a list of two items, sigma and window width "
                        "for gaussian smoothing of profileA "
                        "before computing metrics. Empty list indicates no"
                        "smoothing", default=[])

    parser.add_argument('--smooth-profileB', nargs='+',
                        help="a list of two items, sigma and window width "
                        "for gaussian smoothing of profileB "
                        "before computing metrics. Empty list indicates no"
                        "smoothing", default=[])
    
    parser.add_argument('--countsA', type=str,
                        help="the bigWig with region counts assigned to "
                        "each base (the counts track that is produced by "
                        "the predict script). This is optional.")

    parser.add_argument('--countsB', type=str,
                        help="the bigWig with region counts assigned to "
                        "each base (the counts track that is produced by "
                        "the predict script). This is optional.")

    parser.add_argument('--apply-softmax-to-profileA', action='store_true',
                        help="apply softmax to profileA before computing"
                        "metrics (in casees where profileA is logits)")
    
    parser.add_argument('--apply-softmax-to-profileB', action='store_true',
                        help="apply softmax to profileB before computing"
                        "metrics (in casees where profileB is logits)")

    parser.add_argument('--metrics-seq-len', type=int, 
                        help="the length of the sequence over which to "
                        "compute the metrics", default=1000)
    
    parser.add_argument('--peaks', type=str, 
                        help="the path to the file containing ")

    parser.add_argument('--step-size', type=int,
                        help="the step size for genome wide metrics", 
                        default=50)
    
    parser.add_argument('--chroms', '-c', nargs='+', required=True,
                        help="list of test chromosomes to compute metrics")
    
    # output params
    parser.add_argument('--output-dir', '-o', type=str, required=True,
                        help="destination directory to store metrics results")
    
    parser.add_argument('--automate-filenames', action='store_true', 
                        help="specify if the metrics output should "
                        "be stored in a timestamped subdirectory within "
                        "--output-dir")

    parser.add_argument('--time-zone', type=str,
                        help="time zone to use for timestamping output "
                        "directories", default='US/Pacific')
    
    parser.add_argument('--other-tags', nargs='+',
                        help="list of additional tags to be added as "
                        "suffix to the filenames", default=[])

    # reference params
    parser.add_argument('--chrom-sizes', '-s', type=str, required=True,
                        help="path to chromosome sizes file")
    return parser

def interpret_argsparser():
    """ Command line arguments for the interpret script

        Returns:
            argparse.ArgumentParser
    """
    
    parser = argparse.ArgumentParser()
    
    # input params
    parser.add_argument('--input-seq-len', '-l', type=int, 
                        help="the length of the input sequence to the model", 
                        default=1346)
    
    parser.add_argument('--control-len', type=int, 
                        help="the length of the control input to the model", 
                        default=1000)

    parser.add_argument('--model', '-m', type=str, required=True,
                        help="the path to the model (.h5) file")

    parser.add_argument('--bed-file', '-b', type=str, required=True,
                        help="the path to the bed file containing "
                        "postions at which the model should be interpreted")

    parser.add_argument('--presort-bed-file', action='store_true', 
                        help="specify if the --bed-file should be sorted, "
                        "in descending order of strongest peaks, before "
                        "processing")
    
    parser.add_argument('--sample', type=int,
                        help="the number of samples to randomly sample from "
                        "the bed file")

    parser.add_argument('--chroms', nargs='+',
                        help="list of chroms on which the contribution score "
                        "are to be computed. Empty list implies all "
                        "chromosomes", default=[])

    parser.add_argument('--controls', '-c', nargs='+',
                        help="list of paths to control bigWig files. If "
                        "unstranded specify a single file path, if stranded "
                        "then a plus & minus bigWig file, in that order, must "
                        "be specified.")

    parser.add_argument('--control-smoothing', nargs='+',
                        help="list of smoothing values for control inputs to "
                        "the model", default=[1, 50])
    
    # output params
    parser.add_argument('--output-dir', '-o', type=str, required=True,
                        help="destination directory to store the "
                        "interpretation scores")
    
    parser.add_argument('--time-zone', '-t', type=str,
                        help="time zone to use for timestamping output "
                        "directories", default='US/Pacific')
    
    parser.add_argument('--other-tags', nargs='+',
                        help="list of additional tags to be added as "
                        "suffix to the filenames", default=[])

    #reference params
    parser.add_argument('--reference-genome', '-g', type=str, required=True,
                        help="number of gpus to use", default=1)
    return parser
