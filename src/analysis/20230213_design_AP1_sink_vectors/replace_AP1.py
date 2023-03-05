import sys
from random import choice

_, inp = sys.argv

# find all instances matching ATGA[G|C]TCAT and replace with fixed sequence
with open(inp) as f:
    d = [x.strip() for x in f]

# take second line corresponding to sequence
seq = d[1]

cur_pos = 0
scram_seq = ''
while True:
    find1 = seq.find("ATGAGTCAT", cur_pos) 
    find2 = seq.find("ATGACTCAT", cur_pos)

    if find1 == -1 and find2 == -1:
        break
    elif find1 == -1:
        next_pos = find2
    elif find2 == -1:
        next_pos = find1
    else:
        next_pos = min(find1, find2)

    scram_seq += seq[cur_pos:next_pos]

    # a neutral sequence that doesn't create new binding sites
    scram_seq += choice(["CCCAAACCC", "GGGTTTGGG"])

    cur_pos = next_pos + 9

scram_seq += seq[cur_pos:]

print(scram_seq)
