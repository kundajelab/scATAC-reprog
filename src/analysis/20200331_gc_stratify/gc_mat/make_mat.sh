#!/bin/bash
set -e
set -o pipefail
set -u

INBED=$1
OUTF=$2

fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed <(cat $INBED | awk -v OFS='\t' '{mid=int(($2+$3)/2) ; print $1, mid-500, mid+500}') | \
grep -v chr |   sed  's/[G|C|g|c]/1\t/g'  | sed 's/[A|T|N|n|a|t]/0\t/g' | gzip > $OUTF
