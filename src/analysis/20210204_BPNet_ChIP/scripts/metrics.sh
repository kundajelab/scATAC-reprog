#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20210204_BPNet_ChIP/
RUNNAME=20210204_SOX2
PREDICTIONS_DIR=$BASE/models/$RUNNAME/predictions

mkdir -p $PREDICTIONS_DIR/metrics/plus
mkdir -p $PREDICTIONS_DIR/metrics/minus

python metrics.py \
	-A $BASE/data/SOX2/plus.bw \
	-B $PREDICTIONS_DIR/*/*_plus.bw \
	-c chr1 \
	--peaks $BASE/data/SOX2/peaks.bed \
	-o $PREDICTIONS_DIR/metrics/plus \
	-s /users/surag/genomes/hg38/hg38.chrom.sizes \
	--countsB $PREDICTIONS_DIR/*/*_plus_exponentiated_counts.bw \
	--apply-softmax-to-profileB > $PREDICTIONS_DIR/metrics/plus/log.txt

python metrics.py \
        -A $BASE/data/SOX2/minus.bw \
        -B $PREDICTIONS_DIR/*/*_minus.bw \
        -c chr1 \
        --peaks $BASE/data/SOX2/peaks.bed \
        -o $PREDICTIONS_DIR/metrics/minus \
        -s /users/surag/genomes/hg38/hg38.chrom.sizes \
        --countsB $PREDICTIONS_DIR/*/*_minus_exponentiated_counts.bw \
        --apply-softmax-to-profileB > $PREDICTIONS_DIR/metrics/minus/log.txt
