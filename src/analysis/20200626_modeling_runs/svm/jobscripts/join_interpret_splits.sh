#!/bin/bash
set -e
# set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/svm/
RUNNAME=20200626_gc_matched_negatives
DATA=$BASE/data/20200518_n76052/

for i in {1..18}
 do
  echo $i
  cat $BASE/models/$RUNNAME/cluster_idx$i/interpretation/out/* | gzip > $BASE/models/$RUNNAME/cluster_idx$i/interpretation/joined.hyp.txt.gz & 
done

wait
