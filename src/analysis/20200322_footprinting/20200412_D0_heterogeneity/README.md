cluster6.open.bed was manually derived in `20200319_cell_state_dissection` as a peak set open in one half of the fibroblasts and closed in the other. It is labeled as "cluster6" since it corresponds to Cluster 6 of `clusters_20200122_snapATAC_20200125_n76770`.

`bedtools intersect -a ../beds/TCF21.homer.hg38.bed -b  cluster6.open.bed -u > beds/TCF21.homer.intersect.cluster6.open.bed`
