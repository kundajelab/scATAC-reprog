#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/svm/
RUNNAME=20200626_gc_matched_negatives
DATA=$BASE/data/20200518_n76052/
MODISCO=/scratch/users/surag/scATAC-reprog/svm/jobscripts/run_modisco.py

for i in {15..18}
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/modisco_50k
 done


for i in {15..18}
 do
   sbatch --job-name svm_modisco_c${i} \
         --time 84:00:00 \
         --mem 250G \
         --gres gpu:1 \
         --cores-per-socket 8 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/modisco_50k/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/modisco_50k/err.txt \
         jobscript_modisco.sh python $MODISCO \
         -d $BASE/models/$RUNNAME/cluster_idx$i/interpretation/joined.hyp.txt.gz \
         -f $BASE/models/$RUNNAME/cluster_idx$i/interpretation/peaks.20k.fa  \
         -save $BASE/models/$RUNNAME/cluster_idx$i/modisco_50k ;
 done
