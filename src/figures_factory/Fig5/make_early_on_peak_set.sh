#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20200307_fine_clustering/beds/20210719_gridmap_peakwidthnorm_logplusznorm_4way_assited_n20 
FIBR=/oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz

# making a peak set of peaks not in fibr but present in high OSK and all later states till iPSC
# also excluding any that map to peak set 6,7,8 as they are treated separately
bedtools intersect -a $BASE/all_peaks.bed -b <(cat $BASE/idx6.bed $BASE/idx7.bed $BASE/idx8.bed <(zcat $FIBR | cut -f1-3)) -v > tmp1

for i in 11 14 4 5 6 8
 do
  bedtools intersect -a tmp1 -b /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u > tmp2
  mv tmp2 tmp1
done

mv tmp1 early_on.bed
