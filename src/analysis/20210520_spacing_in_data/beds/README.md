`bedtools intersect -a <(zcat ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx4/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | bedsort | bedtools merge | awk -v OFS='\t' '{mid=int(($2+$3)/2) ; print $1, mid-250,mid+250}') -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -v  > high_OSK.not.fibr.500.bed`

`bedtools intersect -a high_OSK.not.fibr.500.bed -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx14/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  -wa -u > high_OSK.not.fibr.500.and.D2.low_OSK.bed`

`bedtools intersect -a high_OSK.not.fibr.500.bed -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx14/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  -v > high_OSK.not.fibr.500.not.D2.low_OSK.bed`
