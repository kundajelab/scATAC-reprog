from collections import defaultdict
from intervaltree import IntervalTree
import argparse
import math
import tqdm
import gzip

"""
This method takes in a narrowPeak file containing all peaks across samples, 
sorted in decreasing order of importance. It then goes down the file and 
creates a non-overlapping peak set of fixed width. Going down in the order
of decreasing importance, peaks overlapping any exisitng accepted peak are
discarded.
"""

parser = argparse.ArgumentParser()
parser.add_argument("-np", "--narrowPeak", type=str, required=True, help="Input narrowPeak file, peaks sorted in decreasing order of importance (typically 9th column)")
parser.add_argument("-w", "--width", type=int, default=500, help="Width of peak in peak set")
parser.add_argument("-ps", "--peak_score_col", type=int, default=9, help="Column of narrowPeak to be used as score of peak (1-indexed)")
parser.add_argument("-o", "--output", type=str, required=True, help="Output bed file of ranges, unsorted, uncompressed")
args = parser.parse_args()


WIDTH = args.width
HALF_WIDTH = args.width//2
SCORE_COL_IDX = args.peak_score_col - 1

# set of interval trees, one for each chromosome
def return_it():
    return IntervalTree()
t = defaultdict(return_it)

def add_interval(it, start, end, summit, score):
    assert( end-start == WIDTH)
    assert(len(it[start:end])==0)
    it[start:end] = {'summit':summit, 'score': score}

score = math.inf
with gzip.open(args.narrowPeak) as f:
    for x in tqdm.tqdm(f):
        x = x.decode('utf-8').strip().split('\t')
        chrm = x[0]
        summit = int(x[1])+int(x[9])

        if float(x[SCORE_COL_IDX]) > score:
            print("Peaks not sorted by decreasing score")
            exit(1)
        score = float(x[SCORE_COL_IDX])
        
        intersects = sorted(t[chrm][summit-HALF_WIDTH:summit+HALF_WIDTH])

        if len(intersects)==0:
            add_interval(t[chrm], summit-HALF_WIDTH, summit+HALF_WIDTH,
                    summit, score)

with open(args.output, "w") as f:
    for x in t:
        for interval in t[x]:
            # 10 column narrowPeak file
            # 9th column score
            # 10th column summit distance from start
            f.write("{}\t{}\t{}\t.\t.\t.\t.\t.\t{}\t{}\n".format(x, interval.begin,
                interval.end, interval.data['score'], 
                interval.data['summit']-interval.begin))

