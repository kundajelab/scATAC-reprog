#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20210204_BPNet_ChIP/
RUNNAME=20210204_SOX2
PREDICTIONS_DIR=$BASE/models/$RUNNAME/predictions

python predict.py \
    --model $(ls $BASE/models/$RUNNAME/*/*.h5) \
    --chrom-sizes /users/surag/genomes/hg38/hg38.chrom.sizes \
    --chroms chr1 \
    --reference-genome /users/surag/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
    --exponentiate-counts \
    --output-dir $PREDICTIONS_DIR \
    --data-dir $BASE/data/SOX2 \
    --predict-peaks \
    --write-buffer-size 2000 \
    --batch-size 1 \
    --has-control \
    --stranded \
    --automate-filenames
