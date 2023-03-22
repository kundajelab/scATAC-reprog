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
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/predict
 done

cd /home/users/surag/kundajelab/chrombpnet-lite/scripts/

for i in {1..15}
 do
  sbatch --job-name predict_c$i \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/predict/log.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/predict/err.txt \
         --mem 50G \
         --cores-per-socket=2 \
         $JOBSCRIPT predict_to_bigwig.py \
         --bias-model $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*adjusted_bias_model.h5 \
         --chrombpnet-model $(ls $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/*.h5 | tail -1) \
         --regions $DATBASE/peaks/overlap_merged/cluster_idx$i.bed \
         --genome /scratch/users/surag/genomes/hg38.genome.fa \
         --chrom-sizes /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --out-prefix $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/predict/cluster_idx$i \
         --tqdm 1
 done
