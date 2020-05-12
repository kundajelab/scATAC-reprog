## Make BAM from tagAlign

DID NOT USE THIS (since reads are not tn5 shifted):
`for i in 1 7 9 4 ; do bash ../scripts/tn5_shifted_ta_to_unshifted_bam.sh /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200125_n76770/tagAligns/cluster_idx$i.tagAlign.gz ~/genomes/hg38/hg38.chrom.sizes > ./unshifted_bams/cluster_idx$i.unshifted.bam & done`

SIMPLY THIS:
`for i in 1 7 9 4 ; do  bedToBam -i <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200125_n76770/tagAligns/cluster_idx$i.tagAlign.gz | sort -k1,1 -k2,2n) -g  ~/genomes/hg38/hg38.chrom.sizes > ./unshifted_bams/cluster_idx$i.unshifted.bam & done`

## TOBIAS Workflow 

`for i in 1 7 9 4 ; do TOBIAS ATACorrect --bam ./unshifted_bams/cluster_idx$i.unshifted.bam --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --peaks ./beds/idr.merged.200.bed --prefix cluster_idx$i.idr.merged.200 --outdir ATACorrect_bw/ --cores 8 > ./ATACorrect_bw/cluster_idx$i.idr.merged.200.log & done`

`for i in 1 7 9 4 ; do TOBIAS FootprintScores --signal ./ATACorrect_bw/cluster_idx$i.idr.merged.200_corrected.bw   --regions ./beds/idr.merged.200.bed  --output footprint_bw/cluster_idx$i.idr.merged.200.footprint.bw  --cores 8 > footprint_bw/cluster_idx$i.idr.merged.200.log & done`


