To intersect peaks with MEF2C motif hits (used only peak here, not 1000bp extension):

`bedtools intersect -a ../beds/MEF2C.homer.hg38.bed -b ../../20200307_fine_clustering/beds/20200307_gridmap_naive_n15/idx15.bed -u  > beds/MEF2C.homer.intersect.idx15.bed`
