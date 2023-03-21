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

28/02/2023

Unfortunately above sequences can not be synthesized as they are highly repetetive.

Instead generating shorter sequences with 1/3/5 binding sites, flanked by Aval sequence CTCGGG.

For ONE: 
cat seq.modified.txt  | tail -1 | cut -c 1-30 | grep TGAGTCA

Manually:
CTCGGG - 7 flank - ATGAGTCAT - 8 flank - CTCGGG

Also stitched two instances to ensure no motifs after stitching (when stitching remove double CTCGGG).

For THREE:
cat seq.modified.txt  | tail -1 | cut -c 1-90 | grep TGAGTCA

For FIVE:
cat seq.modified.txt  | tail -1 | cut -c 1-150

Same for TEN, TWENTY, THIRTY, FORTY, FIFTY.

Scrambles:
First tried scrambling only motifs but keeping bases intact (i.e. using bases ATGAGTCAT). But doing this creates motifs for FOX, OCT4.

Replacement:
Replace ATGA[G|C]TCAT with either CCCAAACCC or GGGTTTGGG randomly. 

Ensure the scramble doesn't introduce CTCGGG or it's reverse complement.
(e.g. python replace_AP1.py short/30.motif.Aval.txt | grep -e CTCGGG -e CCCGAG)

20 - Removed one case of match with TWIST motif manually.
30 - Removed 1 match to CEBP
40 - removed 1 each to AP1, NFY and ELK
