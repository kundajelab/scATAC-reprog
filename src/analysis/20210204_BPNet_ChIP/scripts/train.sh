#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20210204_BPNet_ChIP/
RUNNAME=20210204_SOX2


python bpnettrainer.py --output-dir $BASE/models/$RUNNAME \
       --splits 1_human_val_test_split \
       --input-dir $BASE/data/SOX2 \
       --chrom-sizes /users/surag/genomes/hg38/hg38.chrom.sizes \
       --reference-genome /users/surag/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta  \
       --threads 10     --epochs 100     --train-peaks \
       --chroms $(for i in {1..22} X Y M ; do echo chr$i ; done ) \
       --automate-filenames --filters 64 --learning-rate 0.004 \
       --input-seq-len 1346 --output-len 1000 \
       --has-control --stranded


