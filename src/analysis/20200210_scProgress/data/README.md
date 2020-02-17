- ```bedtools intersect -a ../../20200122_snapATAC/snapATAC_sessions/20200125_n76770/peaks/bulk.cluster.overlap.merged.200.bed -b ../../20200124_H1_progress/data/H1.hESC.atac.overlap.peaks.liftover.to.hg38.bed -loj -wa -c > H1.hESC.atac.overlap.bulk.cluster.overlap.intersect.bed``` was used to count number of overlap H1-hESC peaks that overlap with each bin in day-wise bulk + cluster-wise bulk overlap bins. 
- A header was added and filename changed to H1.hESC.atac.overlap.bulk.cluster.overlap.intersect.txt
- Though values are not binary, data should be used after binarzing. 

- ```bedtools intersect -a ../../20200122_snapATAC/snapATAC_sessions/20200125_n76770/peaks/bulk.cluster.overlap.merged.200.bed -b <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bulk/croo/D0/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz) -loj -wa -c > D0.overlap.bulk.cluster.overlap.intersect.bed``` was used to count number of overlap D0 peaks (Fibroblast peaks) that overlap with each bin in day-wise bulk + cluster-wise bulk overlap bins. 
- A header was added and filename changed to D0.overlap.bulk.cluster.overlap.intersect.txt
- Though values are not binary, data should be used after binarzing.
