This supersedes 20211118_modisco_breakdown.

It's relying on motif curation from 20211007_motif_consolidation while 20211118_modisco_breakdown re-curated motifs for no good reason.

Env: mtbatchgen

Considering those with at least 50 seqlets:

for i in {1..15}; do python ./fetch_tomtom.py  -m ~/oak/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/chrombpnet/cluster_idx$i/modisco/modisco_results_allChroms_counts.hdf5  -o tomtom/cluster_idx$i.txt -d ../20211007_motif_consolidation/20210820_chrombpnet_lite/tfs_final_w_rep.meme -n 1 -s 50 & done

Manually adjusted by visually inspecting and made changes, saved in `manually_adjusted`. Changes and notes below:

Tried to not change (or annotated as dimers) borderline cases especially when they had low counts.

dimers are named as MOTIFA:MOTIFB (except TEAD-TEAD which came out in iPSC on its own). q-value is set to 0 for those modified.
NB: dimers with the same name can be different due to differences in orientation and spacing!!!

c1:
- pattern_15 set to AP1:TEAD
- pattern_18 set to CREB:TEAD  
- pattern_21 set to AP1:TEAD
- pattern_23 set to CREB:TEAD
- pattern_24 set to AP1:TEAD 
- pattern_25 is actually BHLH but we don't have it in reference, so it's ignored for now (currently matched to wrong motif with high q-val)
- pattern_27 set to AP1:FOX 

c2:
- pattern_8 set to AP1:TEAD  
- pattern_21 set to AP1:TEAD

c3:
- pattern_6 set to AP1:TEAD 
- pattern_21 is likely a motif not in reference (TFE), but has few hits. Ignored for now.

c4:
- pattern_9 set to SOX:SOX 
- pattern_13 set to KLF:KLF
- pattern_16 q-value set to 1 (motif unclear)
- pattern_21 set to OCT-SOX:KLF

c5:
- pattern_10 set to SOX:SOX

c6:
- pattern_9 set to SOX:SOX
- pattern_13 set to TEAD

c7:
- pattern_21 set to RUNX:TEAD
- pattern_24 set to AP1:ETS
- pattern_26 set to CREB:ETS

c8:
- pattern_20 set to OCT:TEAD
- pattern_21 set to SOX:SOX

c9:
- pattern_11 set to OCT-SOX
- pattern_16 set to SOX:SOX
- pattern_21 set to AP1:ETS
- pattern_22 set to CREB:ETS
- pattern_23 set to ETS:ETS

c10:
- pattern_14 set to SOX:SOX
- pattern_15 set to AP1:TEAD
- pattern_16 set to CREB:ETS
- pattern_18 set to AP1:ETS
- pattern_19 q-value set to 1 (wrong match)
- pattern_24 set to ETS:ETS

c11:
- pattern_6 set to KLF:KLF
- pattern_7 set to SOX:SOX
- pattern_8 set to OCT-SOX:KLF
- pattern_9 set to KLF:KLF
- pattern_10 set to OCT-SOX:KLF

c12:
- pattern_8 set to AP1:TEAD
- pattern_10 set to AP1:ETS
- pattern_16 set to AP1:TEAD
- pattern_17 set to CREB:TEAD
- pattern_18 set to AP1:TEAD
- pattern_20 set to CREB:ETS
- pattern_23 set to CREB:TEAD
- pattern_26 q-value set to 1 (wrong match)
- pattern_27 q-value set to 1 (fuzzy motif)
- pattern_28 set to RUNX:TEAD

c13:
- pattern_9 set to KLF:KLF
- pattern_12 set to AP1:KLF

c14:
- pattern_7 set to SOX:SOX
- pattern_9 set to KLF:KLF
- pattern_12 set to SOX
- pattern_14 q-value set to 1 (fuzzy motif)
- pattern_16 set to OCT-SOX:KLF

c15:
- pattern_9 set to SOX:SOX
- pattern_11 set to AP1:KLF
- pattern_15 set to KLF:KLF
- pattern_17 set to CREB:ETS
- pattern_20 set to AP1:OCT
- pattern_26 set to AP1:KLF
- pattern_28 q-value set to 1 (fuzzy motif)
