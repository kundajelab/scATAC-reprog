for i in {1..15}; do python ./fetch_tomtom.py  -m ~/oak/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/chrombpnet/cluster_idx$i/modisco/modisco_results_allChroms_counts.hdf5  -o tomtom/cluster_idx$i.txt -d main_motifs_hocomoco.meme -n 1 & done

Manually adjusted by visually inspecting and made changes, saved in `manually_adjusted`:
- set pattern_2 KLF.SP q-value to 0 for c8 (iPSC)
- set pattern_6 KLF.SP q-value to 0 for c1 (Fibroblasts)
- c11 (high OSK) set pattern_4 to SOX instead of OCTSOX
- c7 set BHLH pattern_2 q-value to 0
