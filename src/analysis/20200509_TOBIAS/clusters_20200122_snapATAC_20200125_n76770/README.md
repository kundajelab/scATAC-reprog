## Make BAM from tagAlign

DID NOT USE THIS (since reads are not tn5 shifted):
`for i in 1 7 9 4 ; do bash ../scripts/tn5_shifted_ta_to_unshifted_bam.sh /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200125_n76770/tagAligns/cluster_idx$i.tagAlign.gz ~/genomes/hg38/hg38.chrom.sizes > ./unshifted_bams/cluster_idx$i.unshifted.bam & done`

SIMPLY THIS:
`for i in 1 7 9 4 ; do  bedToBam -i <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200125_n76770/tagAligns/cluster_idx$i.tagAlign.gz | sort -k1,1 -k2,2n) -g  ~/genomes/hg38/hg38.chrom.sizes > ./unshifted_bams/cluster_idx$i.unshifted.bam & done`

## TOBIAS Workflow 

`for i in 1 7 9 4 ; do TOBIAS ATACorrect --bam ./unshifted_bams/cluster_idx$i.unshifted.bam --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --peaks ./beds/idr.merged.200.bed --prefix cluster_idx$i.idr.merged.200 --outdir ATACorrect_bw/ --cores 8 > ./ATACorrect_bw/cluster_idx$i.idr.merged.200.log & done`

`for i in 1 7 9 4 ; do TOBIAS FootprintScores --signal ./ATACorrect_bw/cluster_idx$i.idr.merged.200_corrected.bw   --regions ./beds/idr.merged.200.bed  --output footprint_bw/cluster_idx$i.idr.merged.200.footprint.bw  --cores 8 > footprint_bw/cluster_idx$i.idr.merged.200.log & done`

`TOBIAS BINDetect --motifs ../../../../resources/JASPAR/JASPAR2020_CORE_vertebrates_non-redundant_pfms_jaspar.txt --signals ./footprint_bw/cluster_idx{1,7,9,4}.idr.merged.200.footprint.bw   --peaks ./beds/idr.merged.200.bed --genome ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta --outdir BINDetect --time-series --cores 40 > BINDetect/BINDetect.log`

To make footprint plots:
`TOBIAS PlotAggregate --TFBS BINDetect/MYC_MA0147.3/beds/MYC_MA0147.3_all.bed --signals ATACorrect_bw/cluster_idx{1,7,9,4}.idr.merged.200_corrected.bw --share_y both --plot_boundaries --signal-on-x --output footprint_plots/MYC_footprint.pdf`
