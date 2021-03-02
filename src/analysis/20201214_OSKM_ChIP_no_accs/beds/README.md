`bedtools intersect -a  ~/oak/GEO/GSE36570/croo/SRR445816/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz -b ../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed -v | cut -f1-3 > OCT4_no_accs.bed`

Non-overlapping with fibroblast but with others
`bedtools intersect -a <(bedtools intersect -a  ~/oak/GEO/GSE36570/croo/SRR445816/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz  -b ~/oak/projects/scATAC-reprog/clusters/20201020_n62402/croo/cluster_idx5/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  -v ) -b ../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed -wa -u | cut -f1-3  > OCT4_no_fib_accs.bed`

`bedtools intersect -a  ~/oak/GEO/GSE36570/croo/SRR445817/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz -b ../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed -v | cut -f1-3 > SOX2_no_accs.bed`

`bedtools intersect -a  ~/oak/GEO/GSE36570/croo/SRR445818/peak/idr_reproducibility/idr.optimal_peak.narrowPeak.gz -b ../../20200122_snapATAC/snapATAC_sessions/20201020_n62402/peaks/overlap.no_iPSC.no_clump.merged.500.bed -v | cut -f1-3 > KLF4_no_accs.bed`
