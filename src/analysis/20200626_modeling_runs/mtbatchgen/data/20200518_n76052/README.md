Commands for files in this directory:
`for i in {1..18} ; do cp /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200518_n76052/bigwigs/cluster_idx$i.bw cluster_idx$i/unstranded.bw & done`

To get unique non-overlapping peaks, intersected summits of overlap peaks of each cell state with peak set created from all cell states combined using the `~/kundajelab/scATAC-reprog/src/processing/20200502_merge_peaks/range_merge.py` script. Peaks have length 2000 bp.:
`for i in {1..18} ; do bedtools intersect -a overlap.with_iPSC.range.2000.2000.bed -b <(zcat /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200518_n76052/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz | awk -v OFS='\t' '{print $1,$2+$10,$2+$10+1}') -wa -u > cluster_idx$i/peaks.bed & done`

27/07/2020:
Now training all models with all peaks, i.e. with `overlap.with_iPSC.range.2000.2000.bed`. This is because models trained on their peaks only have a minimum count across all samples and can't predict loss of counts when motifs are disturbed in peaks with lowest number of counts.

`for i in {1..18} ; do (cd cluster_idx$i  ; ln -s ../overlap.with_iPSC.range.2000.2000.bed  peaks.bed) & done`
