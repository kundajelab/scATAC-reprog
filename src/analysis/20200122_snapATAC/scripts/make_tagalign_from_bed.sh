#!/bin/bash
set -e
set -u
set -o pipefail

# The bed files from snapATAC/snaptools are 4 column fragments and do not have strands, which seems to fail the ATAC-seq pipeline
# Breaking each strand into 2 reads and setting + and - strands for them respectively.
# Also removing chromosomes that do not have "chr" in them

BEDGZ=$1
OUTF=$2

zcat $1 | cut -f1-3 | grep "chr" | grep -v "chrM" | awk -v OFS='\t' '{print $1,$2,int(($2+$3)/2),"N","1000","+" ; print $1,int(($2+$3)/2)+1,$3,"N",1000,"-"}' | gzip > $OUTF
