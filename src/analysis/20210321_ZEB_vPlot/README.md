Consolidateed motifs are motifs intersected with high importance regions (across cell types) and then reduced to non-overlapping motifs. Exact details and scripts are currently at `/srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/`. Subject to change as it's rough and not currently under version control.

`/srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/interpretation/high_imp_regions/README.md` describes how high importance regions are computed.
`/srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/beds` describes formation of consolidated motifs.
 
`fibr.overlap.narrowPeak.gz` are D0 fibroblast overlap peaks.

`zcat /srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/beds/hg38.archetype_motifs.v1.0.consolidated.bed.gz | grep -i snai2 > tmp`
`bedtools intersect -a <(zcat fibr.overlap.narrowPeak.gz  | awk -v OFS='\t' '{print $1,$2+$10-100,$2+$10+100}') -b tmp -wa -wb > fibr.summit.int.SNAI.bed`

Same for CTCF.
