These steps were run on the lab cluster.

# get top positive peaks (candidate positives)
To get unique non-overlapping peaks, intersected ~75k summits of overlap peaks of each cell state with peak set created from all cell states combined using the `~/kundajelab/scATAC-reprog/src/processing/20200502_merge_peaks/range_merge.py` script. This gives approximately 60k peaks per cell state. Peaks have length 1000 bp. These will be used as positive peaks.:
`for i in {1..18} ; do bedtools intersect -a ~/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200518_n76052/peaks/overlap.with_iPSC.range.1000.1000.bed -b <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200518_n76052/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | sort -k9 -nr | head -75000| awk -v OFS='\t' '{print $1,$2+$10,$2+$10+1}') -wa -u > cluster_idx$i/peaks.bed & done`

# get all positive peaks
Intersected all overlap peak summits to get complete set of peaks. This is required so that no negative peak overlaps with any positive peak, even those that don't contain the top 75k summits.
`for i in {1..18} ; do bedtools intersect -a ~/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200518_n76052/peaks/overlap.with_iPSC.range.1000.1000.bed -b <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200518_n76052/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | awk -v OFS='\t' '{print $1,$2+$10,$2+$10+1}') -wa -u > cluster_idx$i/all_peaks.bed & done`

# get fasta for each peak
`for i in {1..18};  do fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed cluster_idx$i/peaks.bed > cluster_idx$i/peaks.fa & done`

# get GC content from fasta for each peak (this script is also in the lab for of the lsgkm repo)
`for i in {1..18} ; do python ~/kundajelab/scATAC-reprog/src/utils/gc_predictor.py -fa cluster_idx$i/peaks.fa -o >(sed 's/-/\t/' | sed 's/:/\t/' > cluster_idx$i/peaks.gc.tsv) & done`

# make a dict chr -> GC -> region for candidate GC matched negatives (used file with GC computed for 1000bp windows spaced by 1000bp (e.g 0-1000, 1000-2000 and so on)
`python ~/kundajelab/surag-scripts/svm-pipeline/preprocessing/make_inputs/get_chrom_gc_region_dict.py  --input_bed ~/genomes/hg38/gc.1000bp.every1000bp.tsv --outf hg38.chr.gc.pkl`

# get GC matched negatives for each positive peak that don't overlap with all peaks of that sample (not just the top candidate positives)
`for i in {1..18} ; do python ~/kundajelab/surag-scripts/svm-pipeline/preprocessing/get_negatives.py --outdir cluster_idx$i/ --neg-pickle hg38.chr.gc.pkl --pos-peaks cluster_idx$i/peaks.gc.tsv --exclude-peaks ./cluster_idx$i/all_peaks.bed  & done`

# verify positive and negative peaks don't overlap (should print 0s)
`for i in {1..18} ; do bedtools intersect -a cluster_idx$i/neg.gc.tsv -b cluster_idx$i/peaks.gc.tsv -wa -u | wc -l ; done`

# remove fasta and fai files (will remake after splitting into train test)
`rm cluster_idx*/*.fa*`

# make train test splits
`for i in {1..18}; do (cat cluster_idx$i/peaks.gc.tsv | awk '$1!="chr1"' > cluster_idx$i/pos.train.tsv ; \
                       cat cluster_idx$i/peaks.gc.tsv | awk '$1=="chr1"' > cluster_idx$i/pos.test.tsv ; \
                       cat cluster_idx$i/neg.gc.tsv | awk '$1!="chr1"' > cluster_idx$i/neg.train.tsv ; \
                       cat cluster_idx$i/neg.gc.tsv | awk '$1=="chr1"' > cluster_idx$i/neg.test.tsv) & done`

# make dir for fasta files
`for i in {1..18}; do mkdir cluster_idx$i/fasta/ ; done`

# make fastas
`for i in {1..18}; do ( \
    for j in pos.train pos.test neg.train neg.test ; do \
        fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed cluster_idx$i/$j.tsv > cluster_idx$i/fasta/$j.fa \
   ; done ) & done`
