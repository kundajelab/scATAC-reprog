#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210820_chrombpnet_lite
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATBASE=$BASE/data/20210818_n62599

for i in {15..15}
 do
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/src

for i in {15..15}
 do
  sbatch --job-name interpret_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/err.txt \
         --mem 100G \
         --time 96:00:00 \
         --cores-per-socket=4 \
         $JOBSCRIPT interpret.py \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --model $(ls $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*.h5 | tail -1) \
         --regions $DATBASE/peaks/overlap_merged/cluster_idx$i.bed \
         --output-dir $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret
 done
