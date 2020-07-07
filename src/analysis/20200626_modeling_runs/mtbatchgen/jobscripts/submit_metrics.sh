#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20200625_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# run code from original copy
cd $BASE/models/$RUNNAME/code

for i in {1..18}
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/metrics
 done

for i in {1..18}
 do
  sbatch --job-name metrics_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/metrics/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/metrics/err.txt \
         $JOBSCRIPT metrics.py \
         -A $BASE/data/20200518_n76052/cluster_idx$i/unstranded.bw \
         -B $BASE/models/$RUNNAME/cluster_idx$i/predictions/*unstranded.bw \
         -c chr1 \
         --peaks $BASE/data/20200518_n76052/cluster_idx$i/peaks.bed \
         -o  $BASE/models/$RUNNAME/cluster_idx$i/metrics \
         -s /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --countsB $BASE/models/$RUNNAME/cluster_idx$i/predictions/*_exponentiated_counts.bw \
         --apply-softmax-to-profileB
 done


