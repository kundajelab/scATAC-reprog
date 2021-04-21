Using clusters 1-14 and 16 (iPSC). Cluster 15 is a clump of cells.

This version uses GC matched negatives for training instead of all peaks across all cell states.

Some steps performed on lab cluster.

Files in this directory:
`for i in {1..14} 16 ; do cp /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20201020_n62402/bigwigs/cluster_idx$i.bw cluster_idx$i/unstranded.bw & done`

(for now they are symlinked to previous version in scratch to avoid duplication)

First get merged peaks for each cell state (in the `peaks` dir). Assuming input size of 2346 will be used by the models and computing accordingly:
`for i in {1..14} 16 ; do (zcat ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | sort -k1,1 -k2,2n |  bedtools merge | awk -v OFS='\t' '{mid=int(($2+$3)/2); print $1,mid-1173,mid+1173,".",".",".",".",".",".", 1173}' >  overlap_merged/cluster_idx$i.bed)&  done`

Next we need to find GC matched negatives for each cell state.

Get fasta sequences for each peak in each cell state
`for i in {1..14} 16;  do fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed overlap_merged/cluster_idx$i.bed > overlap_merged_fasta/cluster_idx$i.fa & done`

Compute gc values:
`for i in {1..14} 16 ; do python ~/kundajelab/scATAC-reprog/src/utils/gc_predictor.py -fa overlap_merged_fasta/cluster_idx$i.fa -o >(sed 's/-/\t/' | sed 's/:/\t/' > overlap_merged_gc_vals/cluster_idx$i.gc.tsv) & done`

Split hg38 into 2346 bp bins:
`(while IFS=" " read -r chr sz ; do printf "$chr\t$sz\n" | awk -v OFS='\t' '{for (i=0; i<int($2/2346) ; i++) {print $1,i*2346,(i+1)*2346}}' ; done < <(cat ~/genomes/hg38/hg38.chrom.sizes  | head -24) ) >  hg38.2346bp.every2346bp.bed`
Get fasta:
`fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed hg38.2346bp.every2346bp.bed > tmp`
Compute GC:
`python ~/kundajelab/scATAC-reprog/src/utils/gc_predictor.py -fa tmp -o >(sed 's/-/\t/' | sed 's/:/\t/' > gc.2346bp.every2346bp.tsv)`

 make a dict chr -> GC -> region for candidate GC matched negatives (used file with GC computed for 2346bp windows spaced by 2346bp (e.g 0-2346, 2346-4692 and so on)
`python ~/kundajelab/surag-scripts/svm-pipeline/preprocessing/get_chrom_gc_region_dict.py  --input_bed gc.2346bp.every2346bp.tsv --outf hg38.chr.gc.pkl`

Get non-overlapping GC matched negatives for each peak (converted to 10 column format for BPNet)
`for i in {1..14} 16 ; do python ~/kundajelab/surag-scripts/svm-pipeline/preprocessing/get_negatives.py --outfile >(awk -v OFS='\t' '{print $1,$2,$3,".",".",".",".",".",".",1173}' > gc_neg/cluster_idx$i.gc.neg.bed) --neg-pickle hg38.chr.gc.pkl --pos-peaks overlap_merged_gc_vals/cluster_idx$i.gc.tsv --exclude-peaks overlap_merged_gc_vals/cluster_idx$i.gc.tsv  & done` 

Verify positive and negative peaks don't overlap (should print 0s)
`for i in {1..14} 16 ; do bedtools intersect -a  overlap_merged/cluster_idx$i.bed -b gc_neg/cluster_idx$i.gc.neg.bed -wa -u | wc -l ; done`

cat peaks with gc matched negatives:
`for i in {1..14} 16 ; do cat overlap_merged/cluster_idx$i.bed gc_neg/cluster_idx$i.gc.neg.bed >  ../cluster_idx$i/peaks.bed ; done`
