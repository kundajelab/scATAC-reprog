import argparse
import fileinput

parser = argparse.ArgumentParser('Removes intervals completely subsumed by another. INPUT BED MUST BE SORTED -k1,1 -k2,2n -k3,3nr !!!')
parser.add_argument("-b", "--bed", required=True, type=str, help="Input BED, must be sorted -k1,1 -k2,2n -k3,3nr. '-' for stdin.")
parser.add_argument("-s", "--subsume_thresh", type=int, default=3, help="The interval that subsumes another must not be wider than this param")

args = parser.parse_args()

class Interval():
    def __init__(self, start, end):
        self.start = start
        self.end = end


cur_chr = None
open_intervals = set()

for line in fileinput.input(args.bed):
    line_split = line.strip().split('\t')
    chrm, start, end = line_split[0], int(line_split[1]), int(line_split[2])

    if chrm != cur_chr:
        # reset
        cur_chr = chrm
        open_intervals = set()

    is_subsumed = False
    
    # collect intervals that are no longer relevant (to delete later)
    expired_intervals = []
    
    for interval in open_intervals:
        # by definition interval will start <= current one (since inputs are sorted -k2,2n)
        assert(interval.start <= start)

        if interval.end >= end:
            if (interval.end-interval.start) - (end-start) <= args.subsume_thresh:
                # skip, it is subsumed by interval
                is_subsumed = True
                break
        elif interval.end < start:
            # interval no long relevant
            expired_intervals.append(interval)

    for interval in expired_intervals:
        open_intervals.remove(interval)

    if not is_subsumed:
        # add to open intervals and print out
        open_intervals.add(Interval(start,end))
        print(line, end='')

