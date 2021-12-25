for m in SOX AP1 ; do bedtools intersect -a $m.bed -b OCTSOX.bed -v > $m.not.OCTSOX.bed ; done 
