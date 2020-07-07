#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20200625_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# run code from copy
cd $BASE/models/$RUNNAME/code

#for i in {1..18}
# do
#  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/interpretation/
# done

for i in {16..18}
 do
  sbatch --job-name interpret_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/interpretation/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/interpretation/err.txt \
         --mem=50G \
         $JOBSCRIPT interpret.py \
         --model $BASE/models/$RUNNAME/cluster_idx$i/*/*.h5 \
         --reference-genome /scratch/users/surag/genomes/hg38.genome.fa \
         --output-dir $BASE/models/$RUNNAME/cluster_idx$i/interpretation \
         -b $BASE/data/20200518_n76052/cluster_idx$i/peaks.bed \
         --input-seq-len 2346  
 done


