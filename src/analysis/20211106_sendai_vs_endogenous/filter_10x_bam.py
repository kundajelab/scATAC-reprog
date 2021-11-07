import fileinput
import sys
import argparse

"""
Filter 10x bam to extract only alignments that are counted in the matrix
for a given gene of interest.

Running this almost always (>99.9%) gives the same counts as in the
matrix. One edge case I saw was when the read is antisense for transcript
of another gene (not to which it is aligned), then it is dropped by this
script (which filters out anything with an antisense tag).

Stream in a bam file with header (-h), and make sure to subset it to
the coordinates of the gene of interest.
"""

parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gene-of-interest", required=True, type=str)
args = parser.parse_args()

for line in sys.stdin: #fileinput.input():
    if line[0]=="@":
        # print header
        print(line.strip())
        continue 

    line_sp = line.split('\t')
    xf = [y.strip().split(":")[2] for y in line_sp if "xf:" in y]
    assert len(xf)==1, xf
    
    antisense = [y.strip().split(":")[2] for y in line_sp if "AN:" in y]
    gn = [y.strip().split(":")[2] for y in line_sp if "GN:" in y]
    bc = [y.strip().split(":")[2] for y in line_sp if "CB:" in y]

    # should be assigned to gene of interest, not antisense and should pass 10x QC (4th bit of xf)
    # more info on xf https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/output/bam

    if len(gn)==1 and gn[0]==args.gene_of_interest and (len(antisense)==0) and ((int(xf[0]) & 8) == 8):
        # replace read name by barcode so that bamToBed can be used with barcode
        print('\t'.join([bc[0].split('-')[0]] + line.strip().split('\t')[1:]))

