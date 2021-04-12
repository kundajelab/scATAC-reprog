`fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed ../../../20200307_fine_clustering/beds/20201211_gridmap_peakwidthnorm_logplusznorm_4way_ordered_n20/width_200bp/idx8.bed > idx8.200.fa`

# Scan with HOMER OCT-SOX motif
`scanMotifGenomeWide.pl OCTSOX.motif  idx8.200.fa > idx8.200.OCTSOX.hits 2> /dev/null`

# make into bed
`cat idx8.200.OCTSOX.hits  | cut -f2- | sed 's/:/\t/' | sed 's/-/\t/' | awk -v OFS='\t' '{print $1,$2+$4-1,$2+$5,$6,$7,$8}' > idx8.200.OCTSOX.bed`

Eyeballed a few of them to see if lie within important areas. Better way to do this would be to reduce scanning threshold and intersect with important regions.

Reduced threshold to 7 and repeated above.

# ZEB hits in fibroblast peaks
Take ZEB called hits that overlap with high importance regions and overlap them with fibroblast peaks.

` bedtools intersect -a <(zcat /srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/beds/hg38.archetype_motifs.v1.0.consolidated.bed.gz | grep -i snai | grep -i zeb) -b  ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u  > ZEB.cluster_idx5.bed`
