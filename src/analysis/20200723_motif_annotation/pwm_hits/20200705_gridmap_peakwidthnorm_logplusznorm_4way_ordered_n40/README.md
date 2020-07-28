### Get TFs

TF list compiled by aggregating all TFs from previous MoDISco runs on SVM and BPNet.

`cat ../20200702_modisco_summarize/data/20200518_n76052/*/*/*/tomtom_matches.homer.tsv  | awk '$3<0.05' | cut -f2 | grep -v match | usu | wc -l`

Removed SCL manually.

### Scan Peaks for Motifs

Custom script to get selected motif PWMs:
`python ../../scripts/extract_motifs_from_homer.py -s tf.homer.list.txt -m ../../../resources/HOMER/custom.motifs -o  selected.homer.motifs.homer`

Scan:
`scanMotifGenomeWide.pl selected.homer.motifs.homer 20200705_gridmap_peakwidthnorm_logplusznorm_4way_ordered_n40.fa -bed > homer.all.hits 2> >(grep Processing > homer.all.log)`

### Consolidate intervals

Sort:
`cat homer.all.hits | sort -k1,1 -k2,2n -k3,3nr > homer.all.sorted.hits`

Remove intervals contained within other intervals:
`cat homer.all.sorted.hits   |python ../../scripts/remove_subsumed_intervals.py -b -  > homer.all.superset.hits`

Convert to BED (bring back to standard chrms):
`cat homer.all.superset.hits  | sed 's/:/\t/' | sed 's/-/\t/' | awk -v OFS='\t' '{print $1, $2+$4-1, $2+$5}' > homer.all.superset.bed`

The intervals in `homer.all.superset.bed` are scored using BPNet. Details in `20200626_modeling_runs` `block_ism` runs.

### Misc (FIMO runs)
Extract motifs:
`for x in `cat tf.homer.list.txt ` ; do outname=$(printf $x | cut -f1 -d"(" | cut -f1 -d"|" | cut -f1 -d"?") ; python ../../scripts/extract_motifs_from_meme.py -s <(printf "$x\n") -m ~/kundajelab/scATAC-reprog/resources/HOMER/homer_motifs.meme.txt -o single_homer_motif_meme/$outname.meme & done`

Run FIMO:
`cat tf.homer.list.txt | cut -f1 -d"(" | cut -f1 -d"|" | cut -f1 -d"?" | xargs -I{} -P 50 fimo -max-stored-scores 10000000   -o fimo_out_pval/{}  single_homer_motif_meme/{}.meme 20200705_gridmap_peakwidthnorm_logplusznorm_4way_ordered_n40.fa`
