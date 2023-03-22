#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599

mkdir -p $BASE/models/$RUNNAME/bias/cluster_idx1/modisco

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for y in profile counts 
   do
    sbatch --job-name modisco_bias_${y} \
         --output $BASE/models/$RUNNAME/bias/cluster_idx1/modisco/log_$y.txt \
         --error $BASE/models/$RUNNAME/bias/cluster_idx1/modisco/err_$y.txt \
         --mem 250G \
         --gres=gpu:0 \
         --time=96:00:00 \
         --cores-per-socket=4 \
         $JOBSCRIPT run_modisco.py \
         --output-dir $BASE/models/$RUNNAME/bias/cluster_idx1/modisco \
         --scores-dir $BASE/models/$RUNNAME/bias/cluster_idx1/interpret \
         --profile_or_counts $y \
         --crop 500 \
         --max-seqlets 50000 
done
