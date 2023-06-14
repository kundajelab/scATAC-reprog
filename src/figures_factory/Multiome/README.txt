bedtools intersect -a <(sed 1d ~/kundajelab/scATAC-reprog/src/figures_factory/Fig5/motif_scans/scans/importance_thresholded/AP1.not.OCTSOX.tsv ) -b ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -v >  AP1.not.fibr.bed 

bedtools intersect -a <(cat ~/kundajelab/scATAC-reprog/src/analysis/20211007_motif_consolidation/20210820_chrombpnet_lite/motifs.importance.thresholded.bed | grep FOSL2 ) -b ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u > AP1.fibr.bed

Numbers for the paper:
----------------------

AP1 instances in fibroblast peaks: `wc -l AP1.fibr.bed`
AP1 instances in xOSK peaks (non fibr): `wc -l AP1.not.fibr.bed`

New instances that belong to early transient peak sets:
`bedtools intersect -a AP1.not.fibr.bed -b ../../analysis/20200307_fine_clustering/beds/20210719_gridmap_peakwidthnorm_logplusznorm_4way_assited_n20/idx{6,7,8}.bed -wa -u | wc -l` 

Fibroblast AP1 instances that close in xOSK and Intermediate (C14 [new_cluster C11]):
`bedtools intersect -a AP1.fibr.bed -b <(zcat  ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx{11,14}/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz) -v | wc -l`
