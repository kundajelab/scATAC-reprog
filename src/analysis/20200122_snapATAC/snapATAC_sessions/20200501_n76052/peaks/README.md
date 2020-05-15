Commands to generate peaks (example for overlap, same for idr).

`zcat ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz > overlap.peaks.bed`
`python ~/kundajelab/heterokaryon-v2/src/utils/truncate_merged_peak_file_to_200bp_around_summit.py --input_bed overlap.peaks.bed  --summit_flank 100 --outf overlap.peaks.200.bed`
`bedtools sort -i overlap.peaks.200.bed  | bedtools merge -i stdin  > overlap.merged.200.bed`

Deleted intermediate files.

Also performed above with `--sumit_flank 200` to give overlap.merged.400.bed. 
