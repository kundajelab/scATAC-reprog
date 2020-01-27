#!/bin/bash
set -e
set -u
set -o pipefail

# The bed files from snapATAC/snaptools are 4 column and do not have strands, which seems to fail the ATAC-seq pipeline
# Also removing chromosomes that do not have "chr" in them

BEDGZ=$1
OUTF=$2

zcat $1 | cut -f1-3 | grep "chr" | grep -v "chrM" | awk -v OFS='\t' '{print $1,$2,$3,"N","1000","+"}' | gzip > $OUTF
