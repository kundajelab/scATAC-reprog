used HOMER's scanMotifGenomeWide.pl to scan with motifs in ../motifs dir.

Using HOMER's output:
`cat high_OSK.not.fibr.500.OCTSOX.scan  |cut -f2- | i2b  | awk -v OFS='\t' '{print $1,$2+$4,$2+$5,$6,$7,$8}'  >  high_OSK.not.fibr.500.OCTSOX.bed`
