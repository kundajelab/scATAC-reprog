#!/bin/bash
set -e
set -u 
set -o pipefail

# originally written by Anna Shcherbina (originally https://github.com/kundajelab/alzheimers_parkinsons/blob/master/form_deseq_matrix/form_matrix_on_one_node.sh)
# modified by Surag Nair

: '
Expects a tab separated metadata file. First line is the header. 
First column must be the name of the sample. tagAlign file locations
should be in TAGALIGN_COL column, and narrowPeak in NARROWPEAK_COL
column. Specify full paths to METADATA_FILE, OUTFILE.
'

WORKDIR=$1
METADATA_FILE=$2
NARROWPEAK_COL=$3
TAGALIGN_COL=$4
OUTFILE=$5

THREADS=20
TRUNCATE_PYTHON_SCRIPT=/users/surag/kundajelab/heterokaryon-v2/src/utils/truncate_merged_peak_file_to_200bp_around_summit.py
MERGE_PYTHON_SCRIPT=/users/surag/kundajelab/scATAC-reprog/src/analysis/20200331_gc_stratify/data/greedy_merge.py

cd $WORKDIR

if [ -f naive_overlap.optimal_set.bed ]
then rm  naive_overlap.optimal_set.bed
fi

if [ -f naive_overlap.optimal_set.sorted.bed ]
then rm naive_overlap.optimal_set.sorted.bed
fi

if [ -f naive_overlap.optimal_set.sorted.merged.bed ]
then rm naive_overlap.optimal_set.sorted.merged.bed
fi

# removing header from metadata
cat ${METADATA_FILE} | awk 'NR>1 {print $0}' > metadata

#get a merged peak file    
for peak_file in `cut -f${NARROWPEAK_COL} metadata | sort | uniq`
do
    zcat $peak_file >> naive_overlap.optimal_set.bed
done

#truncate peaks to 200 bp around summit
python $TRUNCATE_PYTHON_SCRIPT --input_bed naive_overlap.optimal_set.bed --summit_flank 100 --outf naive_overlap.optimal_set.200.bed
bedtools sort -i naive_overlap.optimal_set.200.bed > naive_overlap.optimal_set.sorted.bed

# greedy merge -- keeps only fixed length bins
python $MERGE_PYTHON_SCRIPT naive_overlap.optimal_set.sorted.bed > naive_overlap.optimal_set.sorted.merged.bed
echo "generated merged peak file!"

# get the counts for each sample within each peak 
# get counts only from cut (i.e. 5p end of read)
export numfiles=`cat metadata | wc -l`
echo $numfiles

getcounts () {
 cur_sample_name=`head -n $1 metadata | tail -n1 | cut -f1`
 echo $cur_sample_name > counts.${cur_sample_name}.txt
 echo $cur_sample_name

 # $2 is TAGALIGN_COL passed through xargs
 cur_tagalign=`head -n $1 metadata  | tail -n1 | cut -f$2`

 bedtools coverage -counts -a naive_overlap.optimal_set.sorted.merged.bed \
        -b <(zcat ${cur_tagalign} | awk -v OFS='\t' '{if ($6=="+") {print $1,$2,$2} else {print $1,$3,$3}}' | sort -k1,1 -k2,2n)  -sorted \
        | cut -f4 >> counts.${cur_sample_name}.txt
} 

export -f getcounts

# https://stackoverflow.com/questions/11003418/calling-shell-functions-with-xargs
seq 1 $numfiles | xargs -I{} -P $THREADS bash -c 'getcounts "$@"' _ {} ${TAGALIGN_COL}

# preserve order 
paste `for f in $(cut -f1 metadata) ; do ls counts.$f.txt ; done` > $OUTFILE 

#clean up temporary files                                                                                                                                                            
echo -e $'chrom\tstart\tend' > index
cat index naive_overlap.optimal_set.sorted.merged.bed > tmp1
paste tmp1 $OUTFILE > tmp2
mv tmp2 $OUTFILE 

#clean up
rm metadata
rm tmp1
rm index
rm counts.*.txt
rm naive_overlap.*
