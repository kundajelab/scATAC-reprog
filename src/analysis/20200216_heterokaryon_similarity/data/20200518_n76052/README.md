For read counts:
`bash form_counts_matrix.sh  ../../../20200122_snapATAC/snapATAC_sessions/20200518_n76052/peaks/overlap.no_iPSC.range.200.300.bed metadata.tsv het.nodox.counts.overlap.no_iPSC.range.200.300.tsv`
`bash form_counts_matrix.sh  ../../../20200122_snapATAC/snapATAC_sessions/20200518_n76052/peaks/overlap.no_iPSC.merged.500.bed metadata.tsv het.nodox.counts.overlap.no_iPSC.merge.500.tsv`

For peak overlaps:
`bash form_peaks_matrix.sh ../../../20200122_snapATAC/snapATAC_sessions/20200518_n76052/peaks/overlap.no_iPSC.merged.500.bed peaks.metadata.tsv het.peaks.overlap.no_iPSC.merge.500.tsv`

Note that this reorders the peaks to be in order, which is not the case with the original `overlap.no_iPSC.range.200.300.bed` file.
