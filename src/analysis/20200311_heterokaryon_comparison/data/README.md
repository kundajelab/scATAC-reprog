Idea is to create a matrix of only overlap peaks for select heterokaryon and scATAC-reprog day-wise bulk samples. Assembled metadata manually.

Command to make matrix:
`bash ~/kundajelab/surag-scripts/atac-pipeline/form_counts_matrix.sh /users/surag/kundajelab/scATAC-reprog/src/analysis/20200311_heterokaryon_comparison/data /users/surag/kundajelab/scATAC-reprog/src/analysis/20200311_heterokaryon_comparison/data/metadata.tsv 3 4 /users/surag/kundajelab/scATAC-reprog/src/analysis/20200311_heterokaryon_comparison/data/scATAC.het.counts.txt`

surag-scripts is at e4007057c11168e0e04ee1675530cb64be255326. 

Also tried a similar thing with peaks instead of counts. That didn't work well. Slightly modified (no cutting peak to 5' end, which is done for reads) above script is here as `form_counts_matrix_binary.sh`.
