#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20230119_chrombpnet_lite_folds1_4/fold6
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# splits from https://kundajelab.slack.com/archives/CCQJC4NJK/p1638441148161800?thread_ts=1638301623.154100&cid=CCQJC4NJK

# make a copy of code run 
mkdir -p $BASE/models/$RUNNAME
cp -r /home/users/surag/kundajelab/chrombpnet-lite/src/ $BASE/models/$RUNNAME/chrombpnet-lite

for i in {1..15}
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in {12..15}
 do
  sbatch --job-name train_fold6_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/err.txt \
         --mem 50G \
         $JOBSCRIPT train_chrombpnet.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --bigwig /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20210714_n64913/bigwigs/cluster_idx$i.bw \
         --peaks /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bpnet/data/20210818_n62599/peaks/overlap_merged/cluster_idx$i.bed \
         --nonpeaks /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bpnet/data/20210818_n62599/peaks/gc_neg/cluster_idx$i.gc.neg.bed \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/ \
         --test-chr "chr7" "chr18" "chr14" --val-chr "chr4" "chr15" "chr21" \
         --bias-model /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/bias/cluster_idx1/DFU39.h5 \
         --max-jitter 500 
 done
