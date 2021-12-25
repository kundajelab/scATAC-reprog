`bedtools intersect -a ~/kundajelab/scATAC-reprog/src/analysis/20200307_fine_clustering/beds/20210719_gridmap_peakwidthnorm_logplusznorm_4way_assited_n20/all_peaks.bed -b ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx11/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  -wa -u > peaks.500bp.intersect.highOSK.overlap.bed`


do fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed peaks.500bp.intersect.highOSK.overlap.bed > peaks.500bp.intersect.highOSK.overlap.fa

