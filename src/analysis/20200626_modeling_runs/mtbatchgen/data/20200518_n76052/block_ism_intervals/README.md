All intervals were obtained from `20200723_motif_annotation` after removing subsumed intervals.

Command for each cluster:
`for i in {1..18} ; do bedtools intersect -a all.bed -b ../cluster_idx$i/peaks.bed -wa -u > cluster_idx$i.bed &  done`

Command to generate a "negative" region (positive regions shifted by +/- 50bp that don't overlap with a positive peak) [CHANGE last bed to all.bed]:
`bedtools intersect -a <(cat cluster_idx5.bed | shuf | awk -v OFS='\t'  '{if (NR%2==0) {print $1,$2+50,$3+50} else {print $1,$2-50,$3-50 } }') -b cluster_idx5.bed -v > cluster_idx5_neg.bed`
