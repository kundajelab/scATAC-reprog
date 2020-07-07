HEADER = """MEME version 4

ALPHABET= ACGT

strands: + -

Background letter frequencies
A 0.25 C 0.25 G 0.25 T 0.25

"""

with open("custom.motifs") as f:
    d = [x.strip() for x in f]

starts = [i for i in range(len(d)) if d[i][0]==">"] + [len(d)]
motifs = [d[starts[i]:starts[i+1]] for i in range(len(starts)-1)]

with open("homer_motifs.meme.txt", 'w') as f:
    f.write(HEADER)
    for motif in motifs:
        name = motif[0].split('\t')[1]
        f.write('MOTIF {}\n'.format(name))
        
        f.write('letter-probability matrix: alength= 4 w= {} nsites= 200\n'.format(len(motif)-1))
        f.write('\n'.join(motif[1:]))
        f.write('\nURL none\n\n')
