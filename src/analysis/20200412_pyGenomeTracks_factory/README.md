To generate plots using PyGenomeTracks.

`make_tracks_file --trackFiles $(for i in 1 6 17 18 8 7 14 10 15 9 2 16 13 11 12 3 4 ; do echo /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20200125_n76770/croo/cluster_idx$i/signal/rep1/cluster_idx$i.pval.signal.bigwig ; done ) refGene.gtf -o tracks.ini`

Change max value to fixed:
`cat tracks.ini | sed 's/#max_value = auto/max_value = 40/' > t ; mv t tracks.ini`

Change min value
`cat tracks.ini | sed 's/min_value = 0/min_value = 2/' > t ; mv t tracks.ini`

Change summary method if required:
`cat tracks.ini   | sed 's/summary_method = mean/summary_method = max/' > t ; mv t tracks.ini`

Changed a few settings to display genes manually in tracks.ini.

For some reason, generating plots is slow if refGene contains all the genes. So usually modify refGene to have gene of interest before generating plot.

To generate plot:
`pyGenomeTracks --tracks tracks.ini  --region chr1:26404822-26429835 --outFileName Lin28A.png --title LIN28A`
