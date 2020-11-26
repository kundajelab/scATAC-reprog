## Peak set

Uses the `overlap.no_iPSC.no_clump.merged.500` peak set. Does not include iPSC peaks and so `cluster_idx16` model should not be used for scoring the hits.

## Getting TFs

Get top 3 matches for MoDISco hits from BPNet and SVM 50k, take motifs with >=5 counts
`cat  ../../../../20200702_modisco_summarize/data/20200518_n76052/*/50k/*/tomtom_matches.vierstra.motif_archetypes.tsv | awk '{if ($3<0.05) {print $2}; if ($5<0.05) {print $4}; if ($7<0.05) {print $6}}' |  sed  '/^$/d' | sort | uniq -c | awk '$1>4 {print $2}' > tfs.txt`

Manually added `MYC_HUMAN.H11MO.0.A`.

## Getting Motif (PWM) Hits

Check peaks are sorted:
`sort -k1,1 -k2,2n -c ../../../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed`

Get hits for subset of motifs, intersect with peak set, sort the output. Note k3,3nr flag is important for next step, which is to remove subsumed hits. 
`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/motif_archetypes/hg38.all_motifs.v1.0.bed.gz   | grep -f tfs.txt) -b ../../../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed -wa -u -sorted | sort -k1,1 -k2,2n -k3,3nr > motif.hits.bed`

Removed last column and gzipped file.

Remove intervals contained within other intervals (subsuming interval must not be >4 bases in length) with updated script:
`zcat  motif.hits.bed.gz | python ../../../scripts/remove_subsumed_intervals.py -s 4 -b -  > motif.superset.bed`

