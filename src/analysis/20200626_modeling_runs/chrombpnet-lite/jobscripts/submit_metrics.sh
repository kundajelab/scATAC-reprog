#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599

for i in {1..15}
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in {1..15}
 do
  sbatch --job-name metrics_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics/err.txt \
         --mem 20G \
         --cores-per-socket=2 \
         $JOBSCRIPT metrics.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --bigwig $DATBASE/cluster_idx$i/unstranded.bw \
         --peaks $DATBASE/peaks/overlap_merged/cluster_idx$i.bed \
         --nonpeaks $DATBASE/peaks/gc_neg/cluster_idx$i.gc.neg.bed \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics \
         --test-chr chr1 \
         --bias-model $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*adjusted_bias_model.h5 \
         --chrombpnet-model $(ls $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*.h5 | tail -1)
 done
