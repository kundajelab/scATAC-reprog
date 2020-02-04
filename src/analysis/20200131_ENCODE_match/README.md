Point of this exercise is to compare clusters with existing cell types to annotate them. Here we use the peak set in the matrix compiled by Anna for the atlas resources and count the reads from each cluster pseudo-bulk.

```
bash ../../20200122_snapATAC/scripts/form_cluster_counts_matrix_from_tagAlign.sh /users/surag/kundajelab/scATAC-reprog/src/analysis/20200131_ENCODE_match/data <(sed '1d' /oak/stanford/groups/akundaje/projects/atlas/counts_matrices/atlas.dnase.idr.counts.txt | cut -f1-3) 18 /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_tagAligns/cluster_idx /users/surag/kundajelab/scATAC-reprog/src/analysis/20200131_ENCODE_match/data/encode.idr.peaks.20200125.n76770.cluster.txt
```
