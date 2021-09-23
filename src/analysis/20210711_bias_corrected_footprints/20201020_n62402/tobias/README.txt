It should technically be run only on the peaks of that sample, but right now running on combined peaks of C4 (high OSK) and C5 (Fibr) since I want corrected scores for those.

TOBIAS ATACorrect --bam ../unshifted_bams/cluster_idx4.unshifted.bam --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --peaks ./peaks/overlap.c4.c5.bed --prefix cluster_idx4 --outdir ATACorrect_bw/ --cores 8  > ./ATACorrect_bw/cluster_idx4.log 

TOBIAS ATACorrect --bam ~/oak/projects/scATAC-reprog/bulk/croo/D0/align/rep1/D0_S1_L001_R1_001.merged.nodup.no_chrM_MT.bam --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --peaks ./peaks/overlap.c4.c5.bed --prefix D0 --outdir ATACorrect_bw/ --cores 8  > ./ATACorrect_bw/D0.log &


Misc:
Trained BPNet on GC matched negative regions only for cluster_idx5 for 25k peaks. Trying to evaluate how good TOBIAS is for predicting bias in the same negative (non-peak) regions.

`TOBIAS ATACorrect --bam ../unshifted_bams/cluster_idx5.unshifted.bam --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --peaks ../../../20210721_bias_model/data/peaks.bed --prefix cluster_idx5_gc_neg --outdir ATACorrect_bw/ --cores 8  > ./ATACorrect_bw/cluster_idx5_gc_neg.log `
