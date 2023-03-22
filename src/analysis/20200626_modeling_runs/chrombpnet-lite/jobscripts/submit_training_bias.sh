#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599

# mkdir -p $BASE/models/$RUNNAME

for i in 8
 do
  mkdir -p $BASE/models/$RUNNAME/bias/cluster_idx$i
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in 8
 do
  sbatch --job-name train_bias_c$i \
         --output $BASE/models/$RUNNAME/bias/cluster_idx$i/log.txt \
         --error $BASE/models/$RUNNAME/bias/cluster_idx$i/err.txt \
         --mem 200G \
         $JOBSCRIPT train_bias.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --bigwig $DATBASE/cluster_idx$i/unstranded.bw \
         --peaks $DATBASE/peaks/overlap_merged/cluster_idx$i.bed \
         --nonpeaks $DATBASE/peaks/gc_neg/cluster_idx$i.gc.neg.bed \
         --output-dir $BASE/models/$RUNNAME/bias/cluster_idx$i/ \
         --test-chr "chr1" --val-chr "chr8" "chr10" \
         --max-jitter 100 
 done
