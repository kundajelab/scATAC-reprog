Supp Table Link: `https://static-content.springer.com/esm/art%3A10.1038%2Fs41556-018-0089-0/MediaObjects/41556_2018_89_MOESM4_ESM.xlsx`

Extracted relevant sheets with pandas and liftOver-ed them to hg38.

bedtools intersect -a naive.specific.atac.hg38.bed -b naive.TFAP2C.chip.hg38.bed -v > naive.specific.non.TFAP2C.atac.hg38.bed 
