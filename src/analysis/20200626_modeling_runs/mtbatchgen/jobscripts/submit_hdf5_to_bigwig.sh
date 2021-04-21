#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210414_gc_neg_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# run code from copy
cd $BASE/models/$RUNNAME/code

for i in {1..14} 16 
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/predictions
 done

# NOTE: deliberately using old 20201020_n62402 data peaks, since want to make predictions
# on peaks across all cell states
for i in {1..14} 16
 do
  sbatch --job-name h5_to_bw_c$i \
         --gres=gpu:0 \
         --output $BASE/models/$RUNNAME/cluster_idx$i/interpretation/h5_to_bw_log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/interpretation/h5_to_bw_err.txt \
         $JOBSCRIPT ~/kundajelab/surag-scripts/bpnet-pipeline/importance/importance_hdf5_to_bigwig.py \
         -h5 $BASE/models/$RUNNAME/cluster_idx$i/interpretation/*/counts_scores.h5 \
         -r  $BASE/models/$RUNNAME/cluster_idx$i/interpretation/*/peaks_valid_scores.bed \
         -c  /scratch/users/surag/genomes/hg38.chrom.sizes \
         -o $BASE/models/$RUNNAME/cluster_idx$i/interpretation/counts.importance.bw  \
         -s $BASE/models/$RUNNAME/cluster_idx$i/interpretation/counts.importance.stats.txt -t 1 
 done
