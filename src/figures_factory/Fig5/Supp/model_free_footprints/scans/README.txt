PWM scan (same for OCTSOX and AP1):

for i in 1 11 14 4 5 6 8 ; do scanMotifGenomeWide.pl ../motifs/highOSK.KLF.HOMER.motif ../regions/c$i.fa > >(cut -f2-  | sed 's/:/\t/' | sed 's/-/\t/' | awk -v OFS='\t' '{print $1,$2+$4,$2+$5,$6,$7,$8}' > KLF.c$i.bed) 2> /dev/null & done
