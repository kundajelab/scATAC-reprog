"""Complements lsgkm by producing a prediction file in the same format as lsgkm prediction,
and outputs gc content or CpG observed/expected for each sequence"""

import pyfaidx
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-fa", "--fasta", required=True, type=str, help="input fasta file, each sequence is one entry")
parser.add_argument("-o", "--output", required=True, type=str, help="output file")
parser.add_argument("-m", "--mode", type=str, default="GC", help="GC% (GC) or CpG observed over expected (CpG)")
args = parser.parse_args()

def calc_gc(s):
    return len([x for x in s.lower() if x=='g' or x=='c'])/len(s)

def calc_cpg(s):
    c = s.lower().count('c')
    g = s.lower().count('g')
    cpg = s.lower().count('cg')
    return cpg*len(s)/(c*g)

fa = pyfaidx.Fasta(args.fasta)
f = open(args.output, 'w')

for x in fa:
    if args.mode=="GC":
        val = calc_gc(str(x))
    elif args.mode=="CpG":
        val = calc_cpg(str(x))
    else:
        print("UNSUPPORTED MODE")
        break

    f.write("{}\t{}\n".format(x.name, val))
f.close()

fa.close()
