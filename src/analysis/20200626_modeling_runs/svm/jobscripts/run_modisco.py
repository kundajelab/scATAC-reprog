import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
import deepdish
import modisco.visualization
from modisco.visualization import viz_sequence
import h5py
import numpy as np
import modisco
import modisco.backend
import modisco.nearest_neighbors
import modisco.affinitymat
import modisco.tfmodisco_workflow.seqlets_to_patterns
import modisco.tfmodisco_workflow.workflow
import modisco.aggregator
import modisco.cluster
import modisco.core
import modisco.coordproducers
import modisco.metaclusterers
import modisco.util
import argparse
import gzip 

from modisco.tfmodisco_workflow.seqlets_to_patterns import TfModiscoSeqletsToPatternsFactory
from modisco.tfmodisco_workflow.workflow import TfModiscoWorkflow
from modisco.visualization import viz_sequence

def parse_args():
    parser = argparse.ArgumentParser(description='Arguments for running tf-modisco')
    parser.add_argument("-d","--path_to_hyp_scores", type=str, help="Path to hypothetical scores", required=True)
    parser.add_argument("-f", "--path_to_fasta", type=str, help="Path to sequence fasta", required=True)
    parser.add_argument("-save","--save_path",type=str,default=None,help="Enter a save directory. If not provided, it is saved in the logdir", required=True)
    args = parser.parse_args()
    return args

# functions below courtesy Av
# https://github.com/kundajelab/tfmodisco/blob/ffdc70bf08852a18f41ba684a58f54cbd5f8c1d0/examples/H1ESC_Nanog_gkmsvm/TF%20MoDISco%20Nanog%20-%20No%20MEME%20init.ipynb
def one_hot_encode_along_channel_axis(sequence):
    to_return = np.zeros((len(sequence),4), dtype=np.int8)
    seq_to_one_hot_fill_in_array(zeros_array=to_return,
                                 sequence=sequence, one_hot_axis=1)
    return to_return

def seq_to_one_hot_fill_in_array(zeros_array, sequence, one_hot_axis):
    assert one_hot_axis==0 or one_hot_axis==1
    if (one_hot_axis==0):
        assert zeros_array.shape[1] == len(sequence)
    elif (one_hot_axis==1): 
        assert zeros_array.shape[0] == len(sequence)
    #will mutate zeros_array
    for (i,char) in enumerate(sequence):
        if (char=="A" or char=="a"):
            char_idx = 0
        elif (char=="C" or char=="c"):
            char_idx = 1
        elif (char=="G" or char=="g"):
            char_idx = 2
        elif (char=="T" or char=="t"):
            char_idx = 3
        elif (char=="N" or char=="n"):
            continue #leave that pos as all 0's
        else:
            raise RuntimeError("Unsupported character: "+str(char))
        if (one_hot_axis==0):
            zeros_array[char_idx,i] = 1
        elif (one_hot_axis==1):
            zeros_array[i,char_idx] = 1


def read_in_seqs_and_scores(fa_file, hypimpscores_file):
    seqs = [x.rstrip() for (i,x) in enumerate(open(fa_file)) if i%2==1]
    #filter out any sequences that contain 'N's
    onehot_data = [np.array(one_hot_encode_along_channel_axis(x))
                   for x in seqs if ('N' not in x)]
    #read in the hypothetical importance scores,
    # filter out any sequences that contain 'N's
    unnorm_hyp_impscores = [w[0] for w in zip([
        np.array( [[float(z) for z in y.split(",")]
            for y in x.decode().rstrip().split("\t")[2].split(";")])
        for x in gzip.open(hypimpscores_file)],seqs)
        if 'N' not in w[1]]
    #in the original GkmExplain paper, a normalization of the
    # importance scores and hypothetical importance scores was
    # proposed, as this was empirically observed to improve
    # the signal-to-noise ratio. Here, I will do a
    # similar-in-spirit normalization that also appears to
    # improve the signal-to-noise ratio, but which is more
    # intuitive and better-motivated than the normalization
    # from the gkmexplain paper (the reason I didn't propose it
    # in that paper is simply that I hadn't considered it).
    #The normalization consists of subtracting the mean
    # hypothetical importance across ACGT at each position such
    # that the sum of the hypothetical importance at each position
    # is 0. The intuition is that this highlights the impact of
    # each base on the output **relative to the other bases that
    # could have been present**. The normalized actual importance
    # is simply the normalized hypothetical importance multiplied
    # by the one-hot encoding.
    hyp_impscores = [x - np.mean(x, axis=-1)[:,None] for x in unnorm_hyp_impscores]
    impscores = [x*y for x,y in zip(hyp_impscores, onehot_data)]
    
    return onehot_data, hyp_impscores, impscores


args = parse_args()

base_path = args.save_path
print("Save path is {}".format(base_path))
seqlet_path = os.path.join(base_path,'seqlets_profile.txt')
save_path = os.path.join(base_path,'modisco_results.hdf5')

assert(os.path.exists(args.path_to_hyp_scores))
print("The path to the hypothetical importance scores is {}".format(args.path_to_hyp_scores))

assert(os.path.exists(args.path_to_fasta))
print("The path to fasta is {}".format(args.path_to_fasta))

onehot_data, hyp_impscores, impscores = read_in_seqs_and_scores(
    fa_file=args.path_to_fasta,
    hypimpscores_file=args.path_to_hyp_scores)
print("Num onehot sequences:",len(onehot_data))


tasks = ['task0']
task_to_scores = OrderedDict()
task_to_hyp_scores = OrderedDict()

task_to_scores['task0']  = impscores
task_to_hyp_scores['task0']  = hyp_impscores

# track_set = modisco.tfmodisco_workflow.workflow.prep_track_set(
#     task_names=["task0"], 
#     contrib_scores=task_to_scores, 
#     hypothetical_contribs=task_to_hyp_scores, 
#     one_hot=onehot_data)


tfmodisco_patterns_factory = TfModiscoSeqletsToPatternsFactory(
    trim_to_window_size=20, initial_flank_to_add=5, kmer_len=8, num_gaps=1, 
    num_mismatches=0, final_min_cluster_size=20)

tfmodisco_workflow = modisco.tfmodisco_workflow.workflow.TfModiscoWorkflow(
    #Slight modifications from the default settings
    sliding_window_size=20, flank_size=5, target_seqlet_fdr=0.05, 
    max_seqlets_per_metacluster=50000, 
    seqlets_to_patterns_factory=tfmodisco_patterns_factory)

tfmodisco_results = tfmodisco_workflow(task_names=["task0"], 
                                       contrib_scores=task_to_scores, 
                                       hypothetical_contribs=task_to_hyp_scores, 
                                       one_hot=onehot_data)

if os.path.exists(save_path):
    print("Saved file already exists. Removing it")
    os.remove(save_path)

grp = h5py.File(save_path)
tfmodisco_results.save_hdf5(grp)
print("Saved modisco results to file {}".format(str(save_path)))

print("Saving seqlets to %s" % seqlet_path)
seqlets = \
    tfmodisco_results.metacluster_idx_to_submetacluster_results[0].seqlets
bases = np.array(["A", "C", "G", "T"])
with open(seqlet_path, "w") as f:
    for seqlet in seqlets:
        sequence = "".join(
            bases[np.argmax(seqlet["sequence"].fwd, axis=-1)]
        )
        example_index = seqlet.coor.example_idx
        start, end = seqlet.coor.start, seqlet.coor.end
        f.write(">example%d:%d-%d\n" % (example_index, start, end))
        f.write(sequence + "\n")


print("Saving pattern visualizations")

def save_plot(weights, dst_fname):
    """
    
    """
    print(dst_fname)
    colors = {0:'green', 1:'blue', 2:'orange', 3:'red'}
    plot_funcs = {0: viz_sequence.plot_a, 1: viz_sequence.plot_c, 
                  2: viz_sequence.plot_g, 3: viz_sequence.plot_t}

    fig = plt.figure(figsize=(20, 2))
    ax = fig.add_subplot(111) 
    viz_sequence.plot_weights_given_ax(ax=ax, array=weights, 
                                       height_padding_factor=0.2,
                                       length_padding=1.0, 
                                       subticks_frequency=1.0, 
                                       colors=colors, plot_funcs=plot_funcs, 
                                       highlight={}, ylabel="")

    plt.savefig(dst_fname)
    
patterns = (tfmodisco_results
            .metacluster_idx_to_submetacluster_results[0]
            .seqlets_to_patterns_result.patterns)

for idx,pattern in enumerate(patterns):
    print(pattern)
    print("pattern idx",idx)
    print(len(pattern.seqlets))
    save_plot(pattern["task0_contrib_scores"].fwd, 
              '{}/contrib_{}.png'.format(base_path, idx))
    save_plot(pattern["sequence"].fwd,
              '{}/sequence_{}.png'.format(base_path, idx))
