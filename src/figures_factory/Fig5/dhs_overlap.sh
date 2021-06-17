#!/bin/bash
set -e
set -o pipefail
set -u 

BASE=/users/surag/kundajelab/scATAC-reprog/src/analysis/20200307_fine_clustering/beds/20201211_gridmap_peakwidthnorm_logplusznorm_4way_ordered_n20/width_200bp 
DHS=/users/surag/kundajelab/scATAC-reprog/resources/DHSIndex/DHS_Index_and_Vocabulary_hg38_WM20190703.txt.gz

# check DHS sorted
zcat $DHS | sed 1d | sort -c -k1,1 -k2,2n

for i in {1..20} 
  do
    # verify sorted
    cat $BASE/idx$i.bed | sort -c -k1,1 -k2,2n

    a=$(cat  $BASE/idx$i.bed | wc -l ) 
    b=$(bedtools coverage -a $BASE/idx$i.bed -b <(zcat $DHS | sed 1d) -sorted | awk '$5>50' | wc -l )
    c=$(printf "$b/$a\n" | bc -l) 
    printf "$i\t$c\t$b\t$a\n"
done
