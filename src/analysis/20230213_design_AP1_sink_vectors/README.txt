Downloaded and renamed motifs from HOMER.

E.g. `wget http://homer.ucsd.edu/homer/motif/HomerMotifDB/homerResults/motif402.motif`

fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed <( cat ../../20211007_motif_consolidation/20210820_chrombpnet_lite/importance_thresholded/cluster_idx1.0.99.bed | grep -i fosl2 | grep "ATGA[G|C]TCAT" | shuf | head -150 |  awk -v OFS='\t' '{if ($6=="+") {print $1,$2-8,$3+10} else {print $1,$2-9,$3+9}}') |  awk 'NR%2==0' | tr '\n' ' ' | sed 's/ //g'  > seq.raw.txt 

Copied to seq.modified.txt

Checked for matches using:
`for x in  `ls motifs | grep -v AP1`; do scanMotifGenomeWide.pl motifs/$x seq.modified.txt 2> /dev/null   ; done `
and counted using:
`for x in  `ls motifs`; do n=$(scanMotifGenomeWide.pl motifs/$x seq.modified.txt 2> /dev/null | wc -l) ; printf "$x\t$n\n" ; done | clt | sort -k2nr`

Manually edited sequences in trial.modified.txt to remove off-target hits.

Removed all TTGT/ACAA matches, also ATGCAA. Did it iteratively.
