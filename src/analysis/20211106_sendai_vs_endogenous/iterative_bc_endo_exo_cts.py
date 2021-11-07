import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--endo-only", required=True, help="Mostly/Only endogenous reads file")
parser.add_argument("-x", "--exo-only", required=True, help="Mostly/Only exogenous reads file")
parser.add_argument("-s", "--sample", required=True, help="Current sample, mix of endo and exo")
parser.add_argument("-o", "--outfile", required=True, help="Output file with 3 columns - barcode, endo_counts, exo_counts")
parser.add_argument("-t", "--strand", required=True, help="Orientation of the gene + or -")
parser.add_argument("-e", "--extend-end", type=int, default=0, help="Extend END further beyond (this is required to be set to 1000 for KLF4 only since iPSC is sparse, other samples have reads beyond range)")
args = parser.parse_args()

"""
All files look like this

chr6	31164344	31164494	TCATACTGTGGGAGAG	255	-
chr6	31164357	31164507	CTGTACCAGTCCCGGT	255	-
...
"""

SCHEMA = ['chr', 'start', 'end', 'bc', '-', 'strand']

# look at where the transcript starts in the direction of the gene, i.e. 5'
start_or_end = 'start' if args.strand == '+' else 'end'

endo_only = pd.read_csv(args.endo_only, sep='\t', names=SCHEMA)
exo_only = pd.read_csv(args.exo_only, sep='\t', names=SCHEMA)

ST = min(min(exo_only[start_or_end]), min(endo_only[start_or_end]))
END = max(max(exo_only[start_or_end]), max(endo_only[start_or_end]))+1 + args.extend_end

endo_vec = np.array([0]*(END-ST))
exo_vec = np.array([0]*(END-ST))

vals, cts = np.unique(endo_only[start_or_end], return_counts=True)
endo_vec[vals-ST] = cts

vals, cts = np.unique(exo_only[start_or_end], return_counts=True)
exo_vec[vals-ST] = cts

norm_endo_vec = endo_vec+1
norm_endo_vec = norm_endo_vec/sum(norm_endo_vec)

norm_exo_vec = exo_vec+1
norm_exo_vec = norm_exo_vec/sum(norm_exo_vec)


cur_samp = pd.read_csv(args.sample, sep='\t', names=SCHEMA)
bc2idx = {x:i for i,x in enumerate(set(cur_samp['bc']))}
idx2bc = {idx:bc for bc,idx in bc2idx.items()}
cur_samp['bc_idx'] = [bc2idx[x] for x in cur_samp['bc']]


coord_bc_ct = cur_samp.groupby([start_or_end, 'bc_idx']).size().reset_index(name='counts')

bc_cts_mat = np.zeros((len(bc2idx), END-ST))

bc_cts_mat[coord_bc_ct['bc_idx'], coord_bc_ct[start_or_end] - ST] = coord_bc_ct['counts']

exo_frac_estimate = np.array([0.5]*len(bc2idx))

ITER = 10

per_bc_cts = bc_cts_mat.sum(-1)

for _ in range(ITER):
    cur_exo_prob = np.outer(exo_frac_estimate, norm_exo_vec)
    cur_endo_prob = np.outer((1-exo_frac_estimate), norm_endo_vec)
    
    per_pos_frac_exo = cur_exo_prob/(cur_exo_prob + cur_endo_prob)
    
    exo_frac_estimate = (per_pos_frac_exo * bc_cts_mat).sum(-1)/per_bc_cts

exo_cts = exo_frac_estimate * per_bc_cts
endo_cts = per_bc_cts - exo_cts
bcs = [idx2bc[i] for i in range(len(idx2bc))]

pd.DataFrame({'bc':bcs, 'exo_cts':exo_cts, 'endo_cts':endo_cts}).to_csv(args.outfile, sep='\t')

