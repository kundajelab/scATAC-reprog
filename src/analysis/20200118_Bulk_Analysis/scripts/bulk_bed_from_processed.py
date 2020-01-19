import scanpy as sc
import numpy as np
import argparse

"""The job of this script is to take the processed files which have 
single-cell counts for 2kb binned regions and convert it into a file
with summed counts (output as a BED file with 4th column as summed 
counts)"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", type=str)
parser.add_argument("-o", "--outfile", type=str)
args = parser.parse_args()

d = sc.read_h5ad(args.infile)
row_counts = np.sum(d.X, axis=0).A1

f = open(args.outfile, 'w')
for idx, row in d.var.iterrows():
    f.write("{}\t{}\t{}\t{}\n".format(row['binchr'], row['binstart'], int(row['binend'])-1, int(row_counts[int(idx)])))
f.close()