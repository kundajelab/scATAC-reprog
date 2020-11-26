Using clusters 1-14 and 16 (iPSC). Cluster 15 is a clump of cells.

Files in this directory:
`for i in {1..14} 16 ; do cp /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20201020_n62402/bigwigs/cluster_idx$i.bw cluster_idx$i/unstranded.bw & done`

Each cell state model is trained on union of peaks across all cell states combined using the `~/kundajelab/scATAC-reprog/src/processing/20200502_merge_peaks/range_merge.py` script. Peaks have length 2000 bp-- `overlap.with_iPSC.range.2000.2000.bed`. This is because models trained on their peaks only have a minimum count across all samples and can't predict loss of counts when motifs are disturbed in peaks with lowest number of counts.

`for i in {1..14} 16 ; do (cd cluster_idx$i  ; ln -s ../overlap.with_iPSC.no_clump.range.2000.2000.bed  peaks.bed) & done`

Cluster specific peaks:
`for i in {1..14} 16 ; do bedtools intersect -a overlap.with_iPSC.no_clump.range.2000.2000.bed -b /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz -wa -u > cluster_specific_peaks/cluster_idx${i}_peaks.bed  ; done`
