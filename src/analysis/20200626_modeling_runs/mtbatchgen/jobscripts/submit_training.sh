#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20210414_gc_neg_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh

# make a copy of code run 
mkdir -p $BASE/models/$RUNNAME
cp -r /home/users/surag/kundajelab/mtbatchgen/example/ $BASE/models/$RUNNAME/code

for i in {1..14} 16
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i
 done

cd /home/users/surag/kundajelab/mtbatchgen/example

for i in {1..14} 16
 do
  sbatch --job-name train_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/err.txt \
         --mem 200G \
         $JOBSCRIPT bpnettrainer.py --output-dir $BASE/models/$RUNNAME/cluster_idx$i \
         --splits 1_human_val_test_split \
         --input-dir $BASE/data/20210414_n62402_gcneg/cluster_idx$i \
         --chrom-sizes /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
         --reference-genome /scratch/users/surag/genomes/hg38.genome.fa \
         --threads 10     --epochs 100     --train-peaks \
         --chroms $(cat /scratch/users/surag/genomes/hg38_chroms.txt) \
         --automate-filenames --filters 256 --learning-rate 0.001 \
         --input-seq-len 2346 --output-len 2000
 done


