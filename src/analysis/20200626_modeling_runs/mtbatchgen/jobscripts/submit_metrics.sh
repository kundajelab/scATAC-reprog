#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210414_gc_neg_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# run code from original copy
cd $BASE/models/$RUNNAME/code

for i in 16
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/metrics
 done

# NOTE: deliberately using old 20201020_n62402 data peaks, since want to make predictions
# on peaks across all cell states
for i in 16
 do
  sbatch --job-name metrics_c$i \
         --gres=gpu:0 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/metrics/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/metrics/err.txt \
         $JOBSCRIPT metrics.py \
         -A $BASE/data/20210414_n62402_gcneg/cluster_idx$i/unstranded.bw \
         -B $BASE/models/$RUNNAME/cluster_idx$i/predictions/*unstranded.bw \
         -c chr1 \
         --peaks $BASE/data/20201020_n62402/cluster_idx$i/peaks.bed \
         -o  $BASE/models/$RUNNAME/cluster_idx$i/metrics \
         -s /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --countsB $BASE/models/$RUNNAME/cluster_idx$i/predictions/*_exponentiated_counts.bw \
         --apply-softmax-to-profileB
 done


