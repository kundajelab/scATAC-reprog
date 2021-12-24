#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20200307_fine_clustering/beds/20210719_gridmap_peakwidthnorm_logplusznorm_4way_assited_n20 
DHS=/users/surag/kundajelab/scATAC-reprog/resources/DHSIndex/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz

# check DHS sorted
zcat $DHS | sed 1d | sort -c -k1,1 -k2,2n

for i in {1..20} 
  do
    a=$(cat  $BASE/idx$i.bed | wc -l ) 
    b=$(bedtools coverage -a <(cat $BASE/idx$i.bed | sort -k1,1 -k2,2n) -b <(zcat $DHS | sed 1d) -sorted | awk '$5>100' | wc -l )
#    b=$(bedtools coverage -a <(cat $BASE/idx$i.bed | sort -k1,1 -k2,2n) -b <(zcat $DHS | sed 1d) -sorted | awk '{s+=$5/($3-$2)} END{print s}')
    c=$(printf "$b/$a\n" | bc -l) 
    printf "$i\t$c\t$b\t$a\n"
done
