Downloaded
http://www.repeatmasker.org/genomes/hg38/RepeatMasker-rm405-db20140131/hg38.fa.out.gz

Then:
`zcat hg38.fa.out.gz  | awk -v OFS='\t' 'NR>3 {print $5,$6,$7,$11}' | gzip > hg38.bed.gz`
