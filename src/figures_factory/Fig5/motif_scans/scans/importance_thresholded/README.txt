`for m in SOX AP1 ; do bedtools intersect -a <(sed 1d $m.tsv) -b <(sed 1d OCTSOX.tsv) -v > t ; cat <(head -1 $m.tsv) t > u ; mv u $m.not.OCTSOX.tsv ; rm t ; done`
