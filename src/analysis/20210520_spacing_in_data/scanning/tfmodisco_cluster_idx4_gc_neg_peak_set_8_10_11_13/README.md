used HOMER's scanMotifGenomeWide.pl to scan with motifs in `../motifs/tfmodisco_cluster_idx4_gc_neg_peak_set_8_10_11_13` dir.

Using HOMER's output:
`for x in `ls *.scan` ; do y=$(basename -s ".scan" $x) ; cat $x |cut -f2- | i2b  | awk -v OFS='\t' '{print $1,$2+$4,$2+$5,$6,$7,$8}'  >   $y.bed ; done`

Intersect with at least one base that has top 1%  importance:
`for x in `ls *.bed` ; do y=$(basename -s ".bed" $x) ; bedtools intersect -a $x -b /srv/www/kundaje/surag/scATAC-reprog/clusters/20201020_n62402/interpretation/20210414_gc_neg_filt256_in2346_out2000/high_imp_regions/beds/cluster_idx4.top_oneperc.bed.gz -wa -u > $y.top_oneperc_imp.bed ; done`

Remove SOX hits that overlap with OCTSOX:
`bedtools intersect -a high_OSK.not.fibr.500.SOX.bed -b high_OSK.not.fibr.500.OCTSOX.bed -v > high_OSK.not.fibr.500.SOX.not.OCTSOX.bed `
and
`bedtools intersect -a high_OSK.not.fibr.500.SOX.top_oneperc_imp.bed -b high_OSK.not.fibr.500.OCTSOX.top_oneperc_imp.bed  -v > high_OSK.not.fibr.500.SOX.not.OCTSOX.top_oneperc_imp.bed`
