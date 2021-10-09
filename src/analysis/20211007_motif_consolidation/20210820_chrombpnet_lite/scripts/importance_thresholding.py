import pyBigWig
import argparse
import numpy as np
import tqdm
import pandas as pd
from collections import defaultdict
from modisco.visualization import viz_sequence
from random import randint

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--imp-bigwig", type=str, required=True, help="Bigwig with importance scores")
parser.add_argument("-r", "--imp-regions", type=str, required=True, help="Regions with importance scores. Only summit (2nd + 10th col) is used for centering, width of region is passed separately")
parser.add_argument("-w", "--imp-width", type=int, required=True, help="Width of each region with importance score")
parser.add_argument("-m", "--motif-to-pfm", type=str, required=True, help="2 column tsv, first col has name of motif, second has path to pfm which is a tsv of dim 4 x L")
parser.add_argument("-s", "--scanned-hits", type=str, required=True, help="Bed file with PWM scans. All names should also be in motif-to-pfm. Can specify schema- see scan-schema")
parser.add_argument("-t", "--threshold", type=float, required=True, help="Threshold on importance scores, 0.99 => top 1 percent compared to random regions of same width and possibly taking into account the silhouette of the motif")
parser.add_argument("--no-silhouette", dest='silhouette', action='store_false', help="Don't use motif silhouette (IC transformed values) to scale importance scores")
parser.set_defaults(silhouette=True)
parser.add_argument("-nbg", "--background-num-samples", type=int, default=100000, help="Regions to sample within peaks to construct null of importance scores")
parser.add_argument("-ss", "--scan-schema", type=str, nargs="+", default=['chr', 'start', 'end', 'name', 'score', 'strand', 'seq'], help="Schema for scanned hits file, must contain minimally chr start end name strand")
args = parser.parse_args()

def get_regions(regions_file, crop_width):
    with open(regions_file) as f:
        scored_regions = [x.strip().split('\t') for x in f]

    # importance scores are computed centered at summit (2nd col + 10th col)
    scored_regions = [(x[0], int(x[9])+int(x[1])-crop_width//2, int(x[9])+int(x[1])+crop_width//2) for x in scored_regions]

    return scored_regions


def get_score(bw, chrm, start, end, orientation, weights):
    if weights is not None:
        assert(orientation in ["+", "-"])
        if orientation == "+":
            cur_val = np.sum(np.abs(np.nan_to_num(bw.values(chrm, start,end)) * weights))
        else:
            cur_val = np.sum(np.abs(np.nan_to_num(bw.values(chrm, start,end)) * weights[::-1]))
    else:
        cur_val = np.sum(np.abs(np.nan_to_num(bw.values(chrm, start,end))))

    return cur_val
        

# get perc percentile of importance values for each PWM
# if silhouette- scale importance values by IC scaled per position max
# regs is the regions with importance scores available
def get_perc(bw, regs, perc, ic_weights, N=10000): 
    vals = [] 
    width = pfm.shape[0]

    for _ in tqdm.tqdm(range(N)): 
        i = np.random.randint(0, len(regs)) 
        j = np.random.randint(regs[i][1], regs[i][2]-width)

        if ic_weights is not None:
            cur_or = "+" if randint(0,1)==0 else "-"
            vals.append(get_score(bw, regs[i][0], j, j+width, cur_or, ic_weights))
        else:
            vals.append(get_score(bw, regs[i][0], j, j+width, None, None))

    return np.quantile(vals, perc) 

imp_regions = get_regions(args.imp_regions, args.imp_width) 
imp_bw = pyBigWig.open(args.imp_bigwig)
pfm_paths = pd.read_csv(args.motif_to_pfm, sep='\t', names=['motif', 'pfm_path'])

motif_thresholds = {}
ic_weights = {}
for _,x in pfm_paths.iterrows():
    pfm = np.loadtxt(x['pfm_path']).T
    ic_weights[x['motif']] = viz_sequence.ic_scale(pfm, background=[0.25]*4).max(-1)

    cur_weights = ic_weights[x['motif']] if args.silhouette else None
    motif_thresholds[x['motif']] = get_perc(imp_bw, imp_regions, args.threshold, cur_weights, N=args.background_num_samples)

pwm_hits = pd.read_csv(args.scanned_hits, sep='\t', names=args.scan_schema)

# print(motif_thresholds)
for _,x in tqdm.tqdm(pwm_hits.iterrows(), total=pwm_hits.shape[0]):
    cur_or = x['strand'] if args.silhouette else None
    cur_wts = ic_weights[x['name']] if args.silhouette else None

    cur_score = get_score(imp_bw, x['chr'], x['start'], x['end'], cur_or, cur_wts) 
   
    if cur_score > motif_thresholds[x['name']]:
        print('\t'.join([str(y) for y in list(x) + [cur_score]]))

imp_bw.close()
