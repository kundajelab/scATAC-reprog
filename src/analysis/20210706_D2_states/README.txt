# Merge IDR peaks from fibroblast, high OSK and early intermediate states
zcat ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx{4,5,14}/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz | bedsort | bedtools merge > merged.idr.peaks
