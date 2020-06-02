To get hits:
`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/FIMO-CIS-BP-Homo_sapiens.liftOver.to.hg38.fimo.txt.annotated.bed.gz | awk '$4=="POU5F1"') -b ~/kundajelab/scATAC-reprog/src/analysis/20200307_fine_clustering/beds/20200520_gridmap_peakwidthnorm_n40/raw/all_peaks.bed > OCT4.bed`

Same for KLF4 and SOX2.
