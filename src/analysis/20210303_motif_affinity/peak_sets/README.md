Non-fibroblast peak open in neural like, pre-iPSC and iPSC
`bedtools intersect -a <(bedtools intersect -a <(bedtools intersect -a ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx4/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -v) -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx16/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u ) -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u > open_stay.bed`

`cat open_stay.bed  | awk -v OFS='\t' '{mid=($2+$10); print $1,mid-100,mid+100}' > open_stay.200.bed`

Non-fibroblast open in neural like, till pre-iPSC
`bedtools intersect -a <(bedtools intersect -a ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx4/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -v) -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u  > open_stay_preiPSC.bed`
