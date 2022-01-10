Merge overlap peaks:
for i in 1 11 14 4 5 6 8 ; do zcat ~/oak/projects/scATAC-reprog/clusters/20210714_n64913/croo/cluster_idx$i/peak/overlap_reproducibility/overlap.optimal_peak.narrowPeak.gz  | bedsort | bedtools merge | shuf  > c$i.overlap.merged.bed ;  done

Fasta:
for i in 1 11 14 4 5 6 8  ; do fastaFromBed -fi ~/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta -bed c$i.overlap.merged.bed > c$i.fa & done
