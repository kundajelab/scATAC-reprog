Downloaded `GSE103509_RAW.tar` from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE103509 on 12 May 2020.

Removed non-het samples and placed them in `./raw/`.

Get human genes, get TPM and renormalize:
`for x in $(ls ./raw/) ;do fname=$(echo $x | cut -f1 -d.) ; zcat ./raw/$x   | grep ENSG | awk -v OFS='\t' '{s[$1] = $6} END{for (x in s) {t+=s[x]} ; for (x in s) {print x,(1e6*s[x]/t)}}' > human_tpm/$fname.tpm.txt ; done`

Verify order of genes is consistent:
`for x in $(ls ./human_tpm/) ; do diff <(cat ./human_tpm/$x | cut -f1) <(cat ./human_tpm/GSM2772599_hFb_MRC5_rep1.tpm.txt | cut -f1) ; done`

Pasted TPMs from all files, added GENE names and header names. Some manual steps. Verified for a few genes.

Got Gene names from gProfiler on 13 May 2020: https://biit.cs.ut.ee/gprofiler/convert.
