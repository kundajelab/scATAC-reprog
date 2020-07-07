#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/svm/
RUNNAME=20200626_gc_matched_negatives
DATA=$BASE/data/20200518_n76052/

for i in {1..18}
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i
 done

for i in {1..18}
 do
  sbatch --job-name svm_train_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/err.txt \
         jobscript.sh /home/users/surag/kundajelab/lsgkm/bin/gkmtrain \
         -m 15000 -v 2 -T 16 \
         $DATA/cluster_idx$i/fasta/pos.train.fa \
         $DATA/cluster_idx$i/fasta/neg.train.fa \
         $BASE/models/$RUNNAME/cluster_idx$i/model
 done


