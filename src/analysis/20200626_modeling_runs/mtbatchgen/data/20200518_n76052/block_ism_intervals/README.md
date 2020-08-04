All intervals were obtained from `20200723_motif_annotation` after removing subsumed intervals.

Command for each cluster:
`for i in {1..18} ; do bedtools intersect -a all.bed -b ../cluster_specific_peaks/cluster_idx${i}_peaks.bed -wa -u > cluster_idx$i.bed &  done`

Command to generate a "negative" region (positive regions shifted by +/- 50bp that don't overlap with a positive peak):
`for i in {1..18} ; do bedtools intersect -a <(cat cluster_idx$i.bed | shuf | awk -v OFS='\t'  '{if (NR%2==0) {print $1,$2+50,$3+50} else {print $1,$2-50,$3-50 } }') -b all.bed -v > cluster_idx${i}_neg.bed & done`
