#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20210204_BPNet_ChIP/
RUNNAME=20210204_SOX2
INT_OUT_DIR=$BASE/models/$RUNNAME/intermediate_output

mkdir -p $INT_OUT_DIR

python intermediate_predict.py \
    --model $(ls $BASE/models/$RUNNAME/*/*.h5) \
    --chrom-sizes /users/surag/genomes/hg38/hg38.chrom.sizes \
    --reference-genome /users/surag/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
    --output-dir $INT_OUT_DIR \
    --bed-file <(cat $BASE/data/SOX2/peaks.bed | cut -f1-3 ) \
    --int-layer-name gap \
    --data-dir $BASE/data/SOX2 \
    --batch-size 64  \
    --has-control \
    --stranded > $INT_OUT_DIR/log.txt 
