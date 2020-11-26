#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20201105_all_peaks_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# run code from copy
cd $BASE/models/$RUNNAME/code

for i in {1..14} 16
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/predictions
 done

for i in {1..14} 16
 do
  sbatch --job-name predict_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/predictions/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/predictions/err.txt \
         $JOBSCRIPT predict.py \
         --model $BASE/models/$RUNNAME/cluster_idx$i/*/*.h5 \
         --chrom-sizes /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --chroms chr1 \
         --exponentiate-counts \
         --output-dir $BASE/models/$RUNNAME/cluster_idx$i/predictions \
         --data-dir $BASE/data/20201020_n62402/cluster_idx$i \
         --predict-peaks \
         --reference-genome /scratch/users/surag/genomes/hg38.genome.fa \
         --write-buffer-size 10000 \
         --input-seq-len 2346 --output-len 2000 \
         --batch-size 128
 done


