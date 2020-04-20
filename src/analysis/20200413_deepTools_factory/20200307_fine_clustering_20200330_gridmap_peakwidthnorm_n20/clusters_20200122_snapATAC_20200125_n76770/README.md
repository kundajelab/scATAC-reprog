To make a desired plot, choose the required bigwigs from ../../bigwiglist.tsv into tmp, which contains one bigwig location per line.

`computeMatrix reference-point -R ../beds/idx10.sample.5000.bed ../beds/idx13.sample.5000.bed ../beds/idx17.sample.5000.bed -S $(cat tmp) -a 1000 -b 1000 --referencePoint center --binSize 10 --missingDataAsZero --numberOfProcessors 40 --outFileName deepToolsMatrices/hist.close.mat.gz &`

`plotHeatmap -m deepToolsMatrices/hist.close.mat.gz -o figs/hist.close.pdf --whatToShow 'heatmap and colorbar' --xAxisLabel "" --samplesLabel   'Fib 27me3' 'D5 27me3' 'iPSC 27me3' --colorMap Reds  &`

To align multiple plots in the same order, first plot the reference:
`plotHeatmap -m deepToolsMatrices/close/atac.mat.gz -o figs/close/atac.pdf --outFileSortedRegions deepToolsMatrices/close/atac.order.dtbed --xAxisLabel "" --whatToShow 'heatmap and colorbar'  --samplesLabel D0 D2 iPSC --colorMap plasma &`

use the outFileSortedRegions as `-R` for others and `--sortUsing` "keep", e.g.
`for x in $(ls *txt | grep -v K) ; do fname=$(basename -s ".txt" $x) ; computeMatrix reference-point -R deepToolsMatrices/open/atac.order.dtbed   -S $(cat $x)  -a 1000 -b 1000 --referencePoint center --binSize 10 --missingDataAsZero --numberOfProcessors 10 --outFileName deepToolsMatrices/open/$fname.mat.gz & done`

`plotHeatmap -m deepToolsMatrices/open/het.dn.mat.gz -o figs/open/dn.het.pdf --whatToShow 'heatmap and colorbar' --xAxisLabel "" --sortRegions "keep" --samplesLabel  'het dnAP1 MRC5' 'het dnAP1 CC' 'het dnAP1 3hr' 'het dnAP1 16hr' 'het dnAP1 48hr' --colorMap plasma &`
