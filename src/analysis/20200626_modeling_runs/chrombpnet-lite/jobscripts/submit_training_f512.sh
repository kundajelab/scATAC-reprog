#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599


for i in 1 8
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx${i}_f512
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in 1 8
 do
  sbatch --job-name train_c${i}_f512 \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx${i}_f512/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx${i}_f512/err.txt \
         --mem 200G \
         $JOBSCRIPT train_chrombpnet.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --bigwig $DATBASE/cluster_idx$i/unstranded.bw \
         --peaks $DATBASE/peaks/overlap_merged/cluster_idx$i.bed \
         --nonpeaks $DATBASE/peaks/gc_neg/cluster_idx$i.gc.neg.bed \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx${i}_f512/ \
         --test-chr "chr1" --val-chr "chr8" "chr10" \
         --bias-model $BASE/models/$RUNNAME/bias/cluster_idx1/DFU39.h5 \
         --max-jitter 500 --filters 512
 done
