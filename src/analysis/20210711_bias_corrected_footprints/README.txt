`for i in 4 ; do bash ../../20200509_TOBIAS/scripts/tn5_shifted_ta_to_unshifted_bam.sh /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20201020_n62402/tagAligns/cluster_idx$i.tagAlign.gz ~/genomes/hg38/hg38.chrom.sizes > ./unshifted_bams/cluster_idx$i.unshifted.bam & done`

`rgt-hint tracks --bc --bigWig --organism=hg38 ../unshifted_bams/cluster_idx4.unshifted.bam <(zcat ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx4/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | bedsort | bedtools merge )   --output-prefix=cluster_idx4 `


Fibr:
`rgt-hint tracks --bc --bigWig --organism=hg38 ~/oak/projects/scATAC-reprog/bulk/croo/D0/align/rep1/D0_S1_L001_R1_001.merged.nodup.no_chrM_MT.bam <(zcat ~/oak/projects/scATAC-reprog/bulk/croo/D0/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | bedsort | bedtools merge )   --output-prefix=D0`

Computed over high OSK peaks
`rgt-hint tracks --bc --bigWig --organism=hg38 ~/oak/projects/scATAC-reprog/bulk/croo/D0/align/rep1/D0_S1_L001_R1_001.merged.nodup.no_chrM_MT.bam <(zcat ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx4/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | bedsort | bedtools merge )   --output-prefix=D0.c4.peaks`
