Commands to generate merged peaks (example for overlap, same for idr). This set is used for peak matrix (pmat) UMAP generation.

Without iPSC (`cluster_idx16`) and without clump (`cluster_idx15`):
`find ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | grep -v idx15 | grep -v idx16 | xargs zcat  > overlap.no_iPSC.no_clump.peaks.bed`
`python ~/kundajelab/heterokaryon-v2/src/utils/truncate_merged_peak_file_to_200bp_around_summit.py --input_bed overlap.no_iPSC.no_clump.peaks.bed  --summit_flank 250 --outf overlap.no_iPSC.no_clump.peaks.500.bed`
`bedtools sort -i overlap.no_iPSC.no_clump.peaks.500.bed  | bedtools merge -i stdin  > overlap.no_iPSC.no_clump.merged.500.bed`

Similarly for IDR.

Deleted intermediate files.

## Range SmallPeaks

To get peaks without iPSC peaks and without clump: 
- `find ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | grep -v idx15 | grep -v idx16 | xargs -I{} zcat {} | sort -k9 -nr | gzip > overlap.no_iPSC.no_clump.peaks.qval.sort.narrowPeak.gz`
- `python ~/kundajelab/scATAC-reprog/src/processing/20200502_merge_peaks/range_merge.py -np ./overlap.no_iPSC.no_clump.peaks.qval.sort.narrowPeak.gz -min 200 -max 300 -o ./overlap.no_iPSC.no_clump.range.200.300.bed`

Same for idr.
