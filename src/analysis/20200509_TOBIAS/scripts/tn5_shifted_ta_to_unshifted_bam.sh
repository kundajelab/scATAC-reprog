#!/bin/bash
set -e
set -o pipefail
set -u

# Takes tn5 shifted pipeline output tagAligns, unshifts the reads and outputs
# a bam file to be used as input to TOBIAS
# writes to stdout

TAGALIGN=$1
GENOME=$2

bedToBam -i <(zcat $TAGALIGN | awk -v OFS='\t' '{if ($6=="+") {$2=$2-4} else if ($6=="-") {$3=$3+5} ; print $0}' | sort -k1,1 -k2,2n) -g $GENOME
