`cat intervals.bed | awk -v OFS='\t' '{mid=(($2+$3)/2) ; print $1, mid-250, mid+250}' > intervals.500.bed`

`bedtools coverage -a intervals.500.bed -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz > intervals.500.coverage.fibroblast.bed`

`bedtools coverage -a intervals.500.bed -b ../../../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed > intervals.500.coverage.all.scATAC.bed`

