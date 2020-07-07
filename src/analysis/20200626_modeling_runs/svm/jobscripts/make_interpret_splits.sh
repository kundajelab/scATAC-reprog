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
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/interpretation/fasta_split
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/interpretation/out/

  # pick 20k peaks from each of the top ~60k peaks at random
  # take fasta, merge consecutive lines, shuffle, then unmerge
  cat $DATA/cluster_idx$i/fasta/pos.train.fa $DATA/cluster_idx$i/fasta/pos.test.fa | \
     awk '{printf("%s%s",$0,(NR%2==0)?"\n":"\0")}' | shuf | \
     head -20000 | tr "\0" "\n" > \
     $BASE/models/$RUNNAME/cluster_idx$i/interpretation/peaks.20k.fa ;
  
  # split peaks into smaller chunks to parallelise
  split -l 250 -a3 -d $BASE/models/$RUNNAME/cluster_idx$i/interpretation/peaks.20k.fa $BASE/models/$RUNNAME/cluster_idx$i/interpretation/fasta_split/peaks.20k.fa. ;

done
