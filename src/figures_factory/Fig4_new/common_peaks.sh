#!/bin/bash
set -e
set -u
set -o pipefail

# cell states
for x in 5 4 8 2 7 1 16
  do
    y=/users/surag/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx$x/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz
    zcat  $y  | sort -k1,1 -k2,2n | bedtools merge > tmp/idx$x.bed
done

multiIntersectBed -i tmp/* | awk '$4==7' | cut -f1-3 > common_peaks.bed


