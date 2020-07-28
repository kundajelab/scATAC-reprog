import argparse
import heapq
import fileinput

parser = argparse.ArgumentParser('Removes intervals completely subsumed by another. INPUT BED MUST BE SORTED -k1,1 -k2,2n -k3,3nr !!!')
parser.add_argument("-b", "--bed", required=True, type=str, help="Input BED, must be sorted -k1,1 -k2,2n -k3,3nr. '-' for stdin.")

args = parser.parse_args()

class Interval():
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __lt__(self, other):
        # heap will keep intervals with farthest ends at the top
        return self.end > other.end

cur_chr = None
open_interval_ends_heap = []

for line in fileinput.input(args.bed):
    line_split = line.strip().split('\t')
    chrm, start, end = line_split[0], int(line_split[1]), int(line_split[2])

    if chrm != cur_chr:
        # reset
        cur_chr = chrm
        open_interval_ends_heap = []

    is_subsumed = False
    while open_interval_ends_heap:
        if open_interval_ends_heap[0].end >= end:
             # an open interval potentially subsumes this interval
            if open_interval_ends_heap[0].start <= start:
                # skip, it is subsumed by another interval
                is_subsumed = True
                break 

            else:
                # interval has expired, remove from heap
                # retry with next available interval
                heapq.heappop(open_interval_ends_heap)
        
        else: 
            # no interval subsumes it 
            break

    if not is_subsumed:
        # add to heap
        heapq.heappush(open_interval_ends_heap, Interval(start,end))

        print(line, end='')



