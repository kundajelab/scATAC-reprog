Note that this doesn't include clump of cells (cluster 16) as pipeline was not run for that.

Merged peaks:
`find ../croo/cluster_idx*/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz   | xargs -I{} zcat {} | sort -k9 -nr | gzip > overlap.peaks.qval.sort.narrowPeak.gz`

`zcat overlap.peaks.qval.sort.narrowPeak.gz | awk -v OFS='\t' '{print $1,$2+$10-250,$2+$10+250}' | bedsort | bedtools merge > overlap.peaks.merged.500.bed`

Resolved peaks:
`python ~/kundajelab/scATAC-reprog/src/processing/20210715_resolve_peaks/resolve.py -np  overlap.peaks.qval.sort.narrowPeak.gz -w 500 -o overlap.peaks.resolved.500.bed`
These were sorted.

Resolved peaks accessible in fibr/iPSC:
`bedtools coverage -a overlap.peaks.resolved.500.bed  -b <(zcat ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | awk -v OFS='\t' '{print $1,$2+$10-250,$2+$10+250}') | awk '$14>0.5' | cut -f1-3  > fibr_iPSC_states/overlap.peaks.resolved.500.fibr.bed`
`bedtools coverage -a overlap.peaks.resolved.500.bed  -b <(zcat ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx1/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | awk -v OFS='\t' '{print $1,$2+$10-250,$2+$10+250}') | awk '$14>0.5' | cut -f1-3  > fibr_iPSC_states/overlap.peaks.resolved.500.ipsc.bed`
