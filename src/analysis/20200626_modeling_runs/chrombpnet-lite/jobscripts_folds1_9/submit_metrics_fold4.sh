#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20230119_chrombpnet_lite_folds1_4/fold4
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

for i in {1..15}
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in {1..15}
 do
  sbatch --job-name metrics_fold4_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics/err.txt \
         --mem 20G \
         --time 1:00:00 \
         --cores-per-socket=2 \
         $JOBSCRIPT metrics.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --bigwig /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20210714_n64913/bigwigs/cluster_idx$i.bw \
         --peaks /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bpnet/data/20210818_n62599/peaks/overlap_merged/cluster_idx$i.bed \
         --nonpeaks /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bpnet/data/20210818_n62599/peaks/gc_neg/cluster_idx$i.gc.neg.bed \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/metrics \
         --test-chr "chr5" "chr16" "chrY" \
         --bias-model $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*adjusted_bias_model.h5 \
         --chrombpnet-model $(ls $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*.h5 | tail -1)
 done
