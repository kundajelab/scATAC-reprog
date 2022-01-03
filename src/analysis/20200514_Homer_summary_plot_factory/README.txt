Curated list based on `20211007_motif_consolidation/20210820_chrombpnet_lite/tfs_final.txt`. Found close matches in HOMER database manually. Did some tweaks based on HOMER enrichment lists to include missing ones, based on:

`cat ../20200307_fine_clustering/homer/20210719_gridmap_peakwidthnorm_logplusznorm_4way_assited_n20/*/knownResults.txt | awk '$3<1e-10' | cut -f1 | sort | uniq -c | sort -nr`
