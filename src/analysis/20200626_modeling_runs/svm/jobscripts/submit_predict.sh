#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/svm/
RUNNAME=20200626_gc_matched_negatives
DATA=$BASE/data/20200518_n76052/

for i in {1..3}
 do
  sbatch --job-name svm_predict_pos_c$i \
         --time 12:00:00 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/log.predict.pos.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/err.predict.pos.txt \
         jobscript.sh /home/users/surag/kundajelab/lsgkm/bin/gkmpredict \
         -v 2 -T 16 \
         $DATA/cluster_idx$i/fasta/pos.test.fa \
         $BASE/models/$RUNNAME/cluster_idx$i/model.model.txt \
         $BASE/models/$RUNNAME/cluster_idx$i/predict.pos.test.txt ; \
   sbatch --job-name svm_predict_neg_c$i \
         --time 12:00:00 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/log.predict.neg.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/err.predict.neg.txt \
         jobscript.sh /home/users/surag/kundajelab/lsgkm/bin/gkmpredict \
         -v 2 -T 16 \
         $DATA/cluster_idx$i/fasta/neg.test.fa \
         $BASE/models/$RUNNAME/cluster_idx$i/model.model.txt \
         $BASE/models/$RUNNAME/cluster_idx$i/predict.neg.test.txt;
 done
