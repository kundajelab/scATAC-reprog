All intervals were obtained from `20200723_motif_annotation/pwm_hits/20201020_n62402/overlap.no_iPSC.no_clump.merged.500/motif.superset.bed` which after removing subsumed intervals. Note these do not incude motif hits at iPSC peaks

Command for each cluster:
`for i in {1..14} ; do bedtools intersect -a all.bed -b ../cluster_specific_peaks/cluster_idx${i}_peaks.bed -wa -u > cluster_idx$i.bed &  done`

Since mtbatchgen has memory leaks and exceeds memory limits when run on large files, split into smaller files:
`for i in {1..14} ; do split -l 1000000 -d cluster_idx$i.bed pos_split/cluster_idx$i.bed. ; done`

Command to generate a "negative" region (positive regions shifted by +/- 50bp that don't overlap with a positive peak). Took 1M for each state.:
`for i in {1..14} ; do (bedtools intersect -a <(cat cluster_idx$i.bed | shuf | awk -v OFS='\t'  '{if (NR%2==0) {print $1,$2+50,$3+50} else {print $1,$2-50,$3-50 } }') -b all.bed -v | head -1000000) > cluster_idx${i}_neg.bed & done` 
