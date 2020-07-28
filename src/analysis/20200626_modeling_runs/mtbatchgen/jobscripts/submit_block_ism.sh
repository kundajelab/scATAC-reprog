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
#  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/block_ism
# done

for i in 12 13 15 
 do
  sbatch --job-name block_ism_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/block_ism/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/block_ism/err.txt \
         --mem=200G \
         $JOBSCRIPT block_ism.py \
         --model $BASE/models/$RUNNAME/cluster_idx$i/*/*.h5 \
         --chrom-sizes /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --output-dir $BASE/models/$RUNNAME/cluster_idx$i/block_ism \
         --data-dir $BASE/data/20200518_n76052/cluster_idx$i \
         --reference-genome /scratch/users/surag/genomes/hg38.genome.fa \
         --input-seq-len 2346 --output-len 2000 \
         --bed-file $BASE/data/20200518_n76052/block_ism_intervals/cluster_idx$i.bed \
         --batch-size 64 
 done


