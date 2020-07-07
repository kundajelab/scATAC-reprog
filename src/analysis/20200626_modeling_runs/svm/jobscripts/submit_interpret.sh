#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/svm/
RUNNAME=20200626_gc_matched_negatives
DATA=$BASE/data/20200518_n76052/

for i in {17..18}
 do
  for splt in `ls $BASE/models/$RUNNAME/cluster_idx$i/interpretation/fasta_split/` ;
   do
    echo $splt $i
    sbatch --job-name svm_interpret_c${i}_${splt} \
         --time 24:00:00 \
         --mem 4G \
         --partition akundaje,normal,owners \
         --sockets-per-node 1 \
         --cores-per-socket 1 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/interpretation/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/interpretation/err.txt \
         jobscript.sh /home/users/surag/kundajelab/lsgkm/bin/gkmexplain \
         -v 2 -m 1 \
         $BASE/models/$RUNNAME/cluster_idx$i/interpretation/fasta_split/$splt \
         $BASE/models/$RUNNAME/cluster_idx$i/model.model.txt \
         $BASE/models/$RUNNAME/cluster_idx$i/interpretation/out/$splt ; 
  done
 done
