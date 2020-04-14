To make a desired plot, choose the required bigwigs from ../../bigwiglist.tsv into tmp, which contains one bigwig location per line.

`computeMatrix reference-point -R ../beds/idx10.sample.5000.bed ../beds/idx13.sample.5000.bed ../beds/idx17.sample.5000.bed -S $(cat tmp) -a 1000 -b 1000 --referencePoint center --binSize 10 --missingDataAsZero --numberOfProcessors 40 --outFileName deepToolsMatrices/hist.close.mat.gz &`

`plotHeatmap -m deepToolsMatrices/hist.close.mat.gz -o figs/hist.close.pdf --whatToShow 'heatmap and colorbar'  --samplesLabel   'Fib 27me3' 'D5 27me3' 'iPSC 27me3' --colorMap Reds  &`:wq
