#!/bin/bash
set -e
set -o pipefail
set -u

PEAKS_BED=$1
METADATA=$2
OUTFILE=$3

# get the counts for each sample within each peak
# get counts only from cut (i.e. 5p end of read)
export numfiles=`cat $METADATA | wc -l`
echo $numfiles

getcounts () {
 # $2 is METADATA passed through xargs
 cur_sample_name=`head -n $1 $2 | tail -n1 | cut -f1`
 echo $cur_sample_name > counts.${cur_sample_name}.txt
 echo $cur_sample_name

 cur_tagalign=`head -n $1 $2  | tail -n1 | cut -f2`
 
 # $3 is PEAKS_BED passed through xargs
 bedtools coverage -counts -a <(cat $3 | cut -f1-3 | sort -k1,1 -k2,2n) \
        -b <(zcat ${cur_tagalign} | awk -v OFS='\t' '{if ($6=="+") {print $1,$2,$2} else {print $1,$3,$3}}' | sort -k1,1 -k2,2n)  -sorted \
        | cut -f4 >> counts.${cur_sample_name}.txt
}

export -f getcounts

# https://stackoverflow.com/questions/11003418/calling-shell-functions-with-xargs
seq 1 $numfiles | xargs -I{} -P 20 bash -c 'getcounts "$@"' _ {} ${METADATA} ${PEAKS_BED}

# preserve order
paste `for f in $(cut -f1 $METADATA) ; do ls counts.$f.txt ; done` > $OUTFILE

#clean up temporary files                                                                                                                                                            
echo -e $'chrom\tstart\tend' > index
cat index <(cat ${PEAKS_BED} | cut -f1-3 | sort -k1,1 -k2,2n)  > tmp1
paste tmp1 $OUTFILE > tmp2
mv tmp2 $OUTFILE

#clean up
rm tmp1
rm index
rm counts.*.txt
