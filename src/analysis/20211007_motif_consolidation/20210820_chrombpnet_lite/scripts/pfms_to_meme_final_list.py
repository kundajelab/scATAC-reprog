# from final list with representative motifs (col 3), make a MEME file

import argparse
import numpy as np

HEADER = """MEME version 4

ALPHABET= ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-pfms", type=str,  required=True, help="Third col of form cts2_pattern_11, 4th col has name")
parser.add_argument("-o", "--output-file", type=str, required=True)
args = parser.parse_args()


motifs = []
with open(args.input_pfms) as f:
    for line in f:
        mot = line.strip().split('\t')[2] # form cts2_pattern_11
        mot = mot.split("_")[0] + "/" + "_".join(mot.split("_")[1:]) + ".pfm"
        name = line.strip().split('\t')[3] 
        motifs.append((mot, name))

pfms = []
for m,n in motifs:
    with open("../pfms/" + m) as f:
        p = np.array([[int(y) for y in x.strip().split("\t")] for x in f])
        pfms.append(p)

with open(args.output_file, 'w') as f:
    f.write(HEADER)
    for i in range(len(motifs)):
        f.write('MOTIF {}\n'.format(motifs[i][1]))
        f.write('letter-probability matrix: alength= 4 w= {} nsites= {}\n'.format(len(pfms[i]), pfms[i][0].sum()))
        for j in range(len(pfms[i])):
            f.write("\t".join(["{:.4f}".format(y/pfms[i][j].sum()) for y in pfms[i][j]]) + "\n")
        f.write('URL none\n\n')

