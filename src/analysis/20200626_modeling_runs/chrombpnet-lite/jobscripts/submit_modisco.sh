#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599

for i in {1..15}
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/modisco
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in {1..15}
 do
 for y in profile #counts 
   do
    sbatch --job-name modisco_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/modisco/log_$y.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/modisco/err_$y.txt \
         --mem 250G \
         --gres=gpu:0 \
         --time=96:00:00 \
         --cores-per-socket=4 \
         $JOBSCRIPT run_modisco.py \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/modisco \
         --scores-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret \
         --profile_or_counts $y \
         --crop 500 \
         --max-seqlets 50000 
  done
done
