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
  mkdir -p $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/bigwig
 done

for i in {1..15}
 do
  for y in profile #counts
   do
    sbatch --job-name h5_to_bw_c$i \
         --gres=gpu:0 \
         --mem=50G \
         --time=2:00:00 \
         --cores-per-socket=2 \
         --output $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/bigwig/log_$y.txt \
         --error $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/bigwig/err_$y.txt \
         $JOBSCRIPT /home/users/surag/kundajelab/chrombpnet-lite/scripts/importance_hdf5_to_bigwig.py \
         -h5 $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/${y}_scores.h5 \
         -r  $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/interpreted_regions.bed \
         -c  /scratch/users/surag/genomes/hg38.chrom.sizes \
         -o $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/bigwig/$y.importance.bw  \
         -s $BASE/models/$RUNNAME/chrombpnet/cluster_idx$i/interpret/bigwig/$y.importance.stats.txt -t 1 
 done
done
