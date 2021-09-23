fastaFromBed  -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed <(zcat ~/oak/projects/SMC_ZEB_KD_TomQ/croo/control/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz | cut -f1-3 | shuf | head -5000) > control.idr.5000.fa

ZEB2 homer motif (403) and BATF (22).

scanMotifGenomeWide.pl ZEB2.motif control.idr.5000.fa > ZEB.control.idr.500.txt 2> log.txt  &

cat ZEB.control.idr.500.txt | cut -f2- | sed 's/:/\t/' | sed 's/-/\t/' | awk -v OFS='\t' '{print $1,$2+$4,$2+$5,$6,$7,$8}' > ZEB.control.idr.500.bed

Same for BATF.
