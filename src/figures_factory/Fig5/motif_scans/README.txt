`for m in AP1 KLF OCTSOX SOX ; do scanMotifGenomeWide.pl motifs/$m.adjusted.motif regions/peaks.500bp.intersect.highOSK.overlap.fa > >(cut -f2-  | sed 's/:/\t/' | sed 's/-/\t/' | awk -v OFS='\t' '{print $1,$2+$4,$2+$5,$6,$7,$8}' > scans/raw/$m.bed) 2> /dev/null & done`

Adjusted motifs were obtained using FindThreshold.ipynb.

Importance thresholding is applied using MotifScanImportanceThreshold.ipynb.
