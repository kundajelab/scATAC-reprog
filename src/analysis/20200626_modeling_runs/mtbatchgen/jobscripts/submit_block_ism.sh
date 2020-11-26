#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20201105_all_peaks_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
DATA=20201020_n62402

# run code from copy
cd $BASE/models/$RUNNAME/code

for i in {1..14}
 do
  for f in $(find $BASE/data/$DATA/block_ism_intervals/pos_split/ -name "cluster_idx$i.bed*")
    do
    # assuming filename is cluster_idx$i.bed.xx where xx is split number
    filename=$(basename -- "$f")
    splitno="${filename##*.}"
    DIR=$BASE/models/$RUNNAME/cluster_idx$i/block_ism/split_${splitno}
    mkdir -p $DIR

    sbatch --job-name block_ism_c${i}_s${splitno} \
           --output $DIR/log.txt \
           --error $DIR/err.txt \
           --mem=250G \
           --time=24:00:00 \
           $JOBSCRIPT block_ism.py \
           --model $BASE/models/$RUNNAME/cluster_idx$i/*/*.h5 \
           --chrom-sizes /scratch/users/surag/genomes/GRCh38_EBV.chrom.sizes \
           --output-dir $DIR \
           --data-dir $BASE/data/$DATA/cluster_idx$i \
           --reference-genome /scratch/users/surag/genomes/hg38.genome.fa \
           --input-seq-len 2346 --output-len 2000 \
           --bed-file $f \
           --batch-size 64 
 done
done

