#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/scratch/users/surag/scATAC-reprog/mtbatchgen/
RUNNAME=20200625_filt256_in2346_out2000
JOBSCRIPT=/scratch/users/surag/scATAC-reprog/mtbatchgen/jobscripts/jobscript.sh
MODISCODIR=modisco_2kb_50k

# run code from copy
cd $BASE/models/$RUNNAME/code

for i in {1..18}
 do
  mkdir -p $BASE/models/$RUNNAME/cluster_idx$i/$MODISCODIR/
 done

for i in {1..18}
 do
  sbatch --job-name modisco_c$i \
         --output $BASE/models/$RUNNAME/cluster_idx$i/$MODISCODIR/log.txt \
         --error $BASE/models/$RUNNAME/cluster_idx$i/$MODISCODIR/err.txt \
         --mem=250G \
         --time=36:00:00 \
         $JOBSCRIPT run_modisco.py \
         -d $(find $BASE/models/$RUNNAME/cluster_idx$i/interpretation/* -maxdepth 1 -type d) \
         -p counts \
         -save $BASE/models/$RUNNAME/cluster_idx$i/$MODISCODIR/ ;
 done


