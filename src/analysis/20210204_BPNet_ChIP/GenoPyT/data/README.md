Took SOX2 ChIP-seq peaks that are not accessible in fibroblasts, and split into accessible or not accessible in the time course (beds from `20201214_OSKM_ChIP_no_accs/beds`). Made GenoPyT compatible Intervals file as follows:

`cat <(cat SOX2_no_accs.bed | awk -v OFS='\t' '{print $1,$2,$3,1}') <(cat SOX2_no_fib_accs.bed | awk -v OFS='\t' '{print $1,$2,$3,0}')  | awk -v OFS='\t' '{mid=int(($2+$3)/2); print $1,mid-500,mid+500,$4}' | bedsort | awk -v OFS='\t' '{if (cc!=$1) {cc=$1; s=1} else {s+=1};print $1,$2,$3,s,$4}' > SOX2.labels.tsv`

Added header and bgzipped file.
