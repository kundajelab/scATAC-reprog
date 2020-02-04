#!/bin/bash
set -e
set -u 
set -o pipefail

# originally written by Anna Shcherbina (originally https://github.com/kundajelab/alzheimers_parkinsons/blob/master/form_deseq_matrix/form_matrix_on_one_node.sh)
# modified by Surag Nair

WORKDIR=$1
PEAKS_FILE=$2 # it's a bed file 
NUM_CLUSTERS=$3
CLUSTER_BEDS_PREFIX=$4 # prefix to the clusters e.g. (full path) "...snapATAC_sessions/20200125_n76770/cluster_beds/cluster_idx"
OUTFILE=$5

THREADS=20

cd $WORKDIR

# get the counts for each sample within each peak 
# get counts only from entire fragment 
export numfiles=$NUM_CLUSTERS
echo $numfiles

cut -f1-3 $PEAKS_FILE |  bedtools sort > peaks.sorted.bed

getcounts () {
 cur_sample_name=$1
 echo "cluster${cur_sample_name}" > counts.${cur_sample_name}.txt
 echo $cur_sample_name

 # $2 is CLUSTER_BEDS_PREFIX passed through xargs
 cur_tagalign=$2$1.bed.gz
 echo $cur_tagalign

 bedtools coverage -counts -a peaks.sorted.bed \
        -b <(zcat ${cur_tagalign} | cut -f1-3 | bedtools sort)  -sorted \
        | cut -f4 >> counts.${cur_sample_name}.txt
} 

export -f getcounts

# https://stackoverflow.com/questions/11003418/calling-shell-functions-with-xargs
seq 1 $numfiles | xargs -I{} -P $THREADS bash -c 'getcounts "$@"' _ {} ${CLUSTER_BEDS_PREFIX}

# preserve order 
paste `for x in $(seq 1 $NUM_CLUSTERS) ; do ls counts.$x.txt ; done` > $OUTFILE 

#clean up temporary files                                                                                                                                                            
echo -e $'chrom\tstart\tend' > index
cat index peaks.sorted.bed > tmp1
paste tmp1 $OUTFILE > tmp2
mv tmp2 $OUTFILE 

#clean up
rm peaks.sorted.bed
rm tmp1
rm index
rm counts.*.txt
