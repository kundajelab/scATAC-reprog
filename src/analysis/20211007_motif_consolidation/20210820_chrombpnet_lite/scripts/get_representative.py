# goal is, given a motif cluster, pick the constituent with the most seqlets

import argparse
import numpy as np
import os

parser = argparse.ArgumentParser()
parser.add_argument("--tfs", type=str, required=True, help='2 col TSV, 1st col is cluster name from gimme cluster, 2nd col is TF name')
parser.add_argument("--cluster-key", type=str, required=True, help='gimme cluster cluster_key.txt')
parser.add_argument("--pfms", type=str, required=True, help='Path to directory pfms, which has cts1, cts2..subdir each with pattern_0,1...')
parser.add_argument("-o", "--outfile", type=str, required=True, help='Output file name')
args = parser.parse_args()

with open(args.tfs) as f:
    tfs = [x.strip().split('\t') for x in f]

with open(args.cluster_key) as f:
    cluster_key = {x.strip().split('\t')[0]:x.strip().split('\t')[1].split(',') for x in f}

#print(tfs)
#print(cluster_key)

def get_count(pfms_base, pfm_string):
    # pfms_base : path to pfms dir
    # pfm_string: looks like cts2_pattern_0.
    with open(os.path.join(pfms_base, pfm_string.split("_")[0], "_".join(pfm_string.split("_")[1:]))) as f:
        vals = [x.strip().split('\t') for x in f]

    # all rows contain counts for each position, just sum for first
    return sum([int(x) for x in vals[0]])


for i in range(len(tfs)):
    # cluster with single entry, name contains pattern idx
    if 'pattern' in tfs[i][0]:
        tfs[i].append(tfs[i][0].split(".")[0])

    else:
        cands = cluster_key[tfs[i][0]]
        cts = [get_count(args.pfms, x) for x in cands]
        tfs[i].append(cands[np.argmax(cts)].split(".")[0])
        #tfs[i].append(str(max(cts)))

with open(args.outfile, 'w') as f:
    for x in tfs:
        f.write('\t'.join(x) + '\n')
