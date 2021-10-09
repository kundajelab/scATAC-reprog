import argparse

HEADER = """MEME version 4

ALPHABET= ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input-pfm", type=str,  required=True)
parser.add_argument("-o", "--output-dir", type=str, required=True)
args = parser.parse_args()


lines = []
with open(args.input_pfm) as f:
    for line in f:
        lines.append(line)

lines = ''.join(lines)
motifs_raw = lines.split('>') # split into motifs
motifs_raw = [x.split('\n') for x in motifs_raw]

motifs = {}
for x in motifs_raw:
    if len(x)>1:
        motifs[x[0]] = [y for y in x[1:] if y!='']

for motif_name in motifs:
    with open("{}/{}.meme".format(args.output_dir, motif_name), 'w') as f:
        f.write(HEADER)
        f.write('MOTIF {}\n'.format(motif_name))
        f.write('letter-probability matrix: alength= 4 w= {} nsites= 200\n'.format(len(motifs[motif_name])))
        f.write('\n'.join(motifs[motif_name]))
        f.write('\nURL none\n\n')

