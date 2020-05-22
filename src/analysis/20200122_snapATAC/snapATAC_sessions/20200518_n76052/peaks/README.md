Commands to generate merged peaks (example for overlap, same for idr). This set is used for peak matrix (pmat) UMAP generation.

Without iPSC (`cluster_idx18`):
`find ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | grep -v idx18 | xargs zcat  > overlap.no_iPSC.peaks.bed`
`python ~/kundajelab/heterokaryon-v2/src/utils/truncate_merged_peak_file_to_200bp_around_summit.py --input_bed overlap.no_iPSC.peaks.bed  --summit_flank 250 --outf overlap.no_iPSC.peaks.500.bed`
`bedtools sort -i overlap.no_iPSC.peaks.500.bed  | bedtools merge -i stdin  > overlap.no_iPSC.merged.500.bed`

Similarly for IDR.

Deleted intermediate files.

## Range SmallPeaks

To get peaks without iPSC peaks: 
- ` find ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | grep -v idx18 | xargs -I{} zcat {} | sort -k9 -nr | gzip > overlap.no_iPSC.peaks.qval.sort.narrowPeak.gz `
