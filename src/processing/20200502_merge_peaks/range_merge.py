from collections import defaultdict
from intervaltree import IntervalTree
import argparse
import math
import tqdm
import gzip

"""
This method takes in a narrowPeak file containing all peaks across samples, 
sorted in decreasing order of importance. It then goes down the file and 
creates a non-overlapping peak set such that the peak widths are within a user
specified range. Logic:

Start with an empty set of merged_peaks.

For each line in the narrowPeak, considers the summit = column 2 + column 10:
- If no existing peak in summit-HALF_MIN_WIDTH, summit+HALF_MIN_WIDTH, make a 
  new peak for that interval.
- Else If intersect with one interval only (say left):
    - if summit lies within existing interval extend overlapping interval as far
      right as possible
    - otherwise try to make a new interval of width MIN_WIDTH from the end of 
      previous interval. If overlap with another interval on the right, follow
      intersection with two intervals (below).
- Else If intersect with 2 intervals:
    - extend existing closest interval (say left) as far right as possible, 
      till it either reaches MAX_WIDTH or hits the beginning of the right 
      interval. Then extend the right interval as far left as possible.

For each peak in the final set, stores the summit position and score of the 
strongest constituent peak.
"""

parser = argparse.ArgumentParser()
parser.add_argument("-np", "--narrowPeak", type=str, required=True, help="Input narrowPeak file, peaks sorted in decreasing order of importance (typically 9th column)")
parser.add_argument("-min", "--min_width", type=int, default=200, help="Minimum width of peak in peak set")
parser.add_argument("-max", "--max_width", type=int, default=400, help="Maximum width of peak in peak set")
parser.add_argument("-ps", "--peak_score_col", type=int, default=9, help="Column of narrowPeak to be used as score of peak (1-indexed)")
parser.add_argument("-o", "--output", type=str, required=True, help="Output bed file of ranges, unsorted, uncompressed")
args = parser.parse_args()

assert(args.min_width<args.max_width)

MIN_WIDTH = args.min_width
MAX_WIDTH = args.max_width
HALF_MIN_WIDTH = int(args.min_width/2)
HALF_MAX_WIDTH = int(args.max_width/2)
SCORE_COL_IDX = args.peak_score_col - 1


def add_interval(it, start, end, summit, score):
    assert(MIN_WIDTH<= end-start <= MAX_WIDTH)
    assert(len(it[start:end])==0)
    it[start:end] = {'summit':summit, 'score': score}


def extend_interval(it, cur_interval, new_start, new_end):
    # since peaks are sorted by decreasing score, there can not be a 
    # case in which extend an interval will decrease its score
    assert(cur_interval in it)
    it.remove(cur_interval) 
    add_interval(it, new_start, new_end, cur_interval.data['summit'],
                cur_interval.data['score'])


def resolve_single_overlap(it, summit, score, intersects):
    assert(len(intersects)==1)
    cur_intersect = intersects[0]

    # merge if summit lies witin existing
    if cur_intersect.begin <= summit < cur_intersect.end: 
        new_min, new_max = cur_intersect.begin, cur_intersect.end

        if summit-HALF_MIN_WIDTH < cur_intersect.begin:
            new_min = max(summit-HALF_MIN_WIDTH, cur_intersect.end-MAX_WIDTH)
        elif summit+HALF_MIN_WIDTH >= cur_intersect.end:
            new_max = min(summit+HALF_MIN_WIDTH, cur_intersect.begin+MAX_WIDTH)
        
        extend_interval(it, cur_intersect, new_min, new_max)

    else:
        # not possible to merge, try to make a new one
        if cur_intersect.begin <= summit-HALF_MIN_WIDTH:
            new_min, new_max = cur_intersect.end, cur_intersect.end + MIN_WIDTH
        else:
            new_min, new_max = cur_intersect.begin - MIN_WIDTH, cur_intersect.begin
        
        # check if this intersects with another
        new_intersect = sorted(it[new_min:new_max])
        if not new_intersect:
            # safe to add
            add_interval(it, new_min, new_max, summit, score)
        
        else:
            # treat like double overlap
            assert(len(new_intersect)==1)
            resolve_double_overlap(it, summit, sorted([cur_intersect, new_intersect[0]]))


def resolve_double_overlap(it, summit, intersects):
    # summit +/- HALF_MIN_WIDTH need not overlap with intersects since they may
    # come from a call from resolve_single_overlap
    assert(len(intersects)==2)
    left_intersect, right_intersect = sorted(intersects)

    # let nearest extend first
    if summit - left_intersect.end < right_intersect.begin - summit:
        # extend left first
        new_left_end = min(left_intersect.begin+MAX_WIDTH, right_intersect.begin)
        new_right_begin = max(new_left_end, right_intersect.end-MAX_WIDTH)
    else:
        new_right_begin = max(left_intersect.end, right_intersect.end-MAX_WIDTH)
        new_left_end = min(new_right_begin, left_intersect.begin+MAX_WIDTH)
   
    extend_interval(it, left_intersect, left_intersect.begin, new_left_end)
    extend_interval(it, right_intersect, new_right_begin, right_intersect.end)


# set of interval trees, one for each chromosome
def return_it():
    return IntervalTree()
t = defaultdict(return_it)

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
        
        intersects = sorted(t[chrm][summit-HALF_MIN_WIDTH:summit+HALF_MIN_WIDTH])

        if len(intersects)==0:
            add_interval(t[chrm], summit-HALF_MIN_WIDTH, summit+HALF_MIN_WIDTH,
                    summit, score)
        elif len(intersects)==1:
            # may lead to creation of new peak, pass score
            resolve_single_overlap(t[chrm], summit, score, intersects)
        else:
            # no score passed since it would not lead to creation of new peak
            resolve_double_overlap(t[chrm], summit, intersects)

with open(args.output, "w") as f:
    for x in t:
        for interval in t[x]:
            # 10 column narrowPeak file
            # 9th column score
            # 10th column summit distance from start
            f.write("{}\t{}\t{}\t.\t.\t.\t.\t.\t{}\t{}\n".format(x, interval.begin,
                interval.end, interval.data['score'], 
                interval.data['summit']-interval.begin))

