H1 is iPSC sample.

In the steps below, we go from ENCODE DCC bulk atac-seq-pipeline outputs (bam and tagAlign) to snap files suitable for SnapATAC. The main issue is that barcodes for each read are not readily available in the outputs, but are there in the fastqs, and hence need to be extracted. Another issue is that the bam file and the tagAlign files do not have reads in the same order. This can be solved by doing a `samtools sort -n` on the bams, which gives the same order as the tagAligns. However to speed things up, instead I do a sort -V on the first column of the bam file (names). This seems to arrange them in the same order. 

The pipeline first sort -V on the bam read names to get a list of sorted read names. Then uses a custom script extract_barcode.py to go through the R2 fastqs and extract the barcode for each read name. The read names are then appended to the tagAlign as an extra column. In addition, a 4 column bed file is made that contains only the 5p ends of the reads, and barcode names. There's another file which is the same as previous but sorted by 4th column (barcode). This file is used to generate the snap file. Another command is run to generate the 5000 and 10000 bp binned peak matrices.


Take bam from pipeline output and extract names of reads, sort by name (sort -V). This seems to do what `samtools sort -n` does, and the tagAlign follows from the name shuffled bam file. Verified `sort -V` matches output from `samtools sort -n` for D2 samples. Command as follows:
`for x in `find /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bulk/croo/*/align/ | grep "MT.bam"` ; do fname=$(basename -s ".bam" $x) ; samtools view $x | cut -f1 | sort -V | gzip >  /srv/scratch/surag/scATAC-reprog/mysnap/$fname.names.sorted.txt.gz  & done`

Used a custom script to extract barcodes for each name in file above. extract_barcode.py first collects all the names that need to be matched to a barcode. Then it goes through all the R2 files (barcode files) and extracts barcodes for the ones required, and then writes them out:
`for x in D0 D2 D4 D6 D8 D10 D12 D14 H1 ; do echo $x ;  names=$(find /srv/scratch/surag/scATAC-reprog/mysnap/$x*sorted.txt.gz) ; echo $names ;  python extract_barcode.py -r $names -f /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/fastq/$x/ -o /srv/scratch/surag/scATAC-reprog/mysnap/$x.barcodes.txt.gz ; done`

To go from tagAlign (pipeline output) + barcodes (one for each line in tagAlign) to 3 files : first is tagAlign and barcode pasted, 2nd is only 5prime with barcode, 3rd is 2nd file but sorted by barcode-
`for x in D0 D2 D4 D6 D8 D10 D12 D14 H1 ; do ta=$(find /oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/bulk/croo/$x/align/rep1/ | grep "tn5.tagAlign.gz") ; tabase=$(basename -s ".tn5.tagAlign.gz" $ta) ;  fname=$(basename -s ".gz" $ta) ; barcode=$(ls /srv/scratch/surag/scATAC-reprog/mysnap/$x.barcodes.txt.gz); echo $x ; echo $ta ; echo $barcode; echo $tabase ;paste <(zcat $ta) <(zcat $barcode)  | tee >(gzip > /srv/scratch/surag/scATAC-reprog/mysnap/$tabase.tn5.withBarcode.tagAlign.gz)  | awk -v OFS='\t' '{if ($6=="+") {print $1,$2,$2+1,$7} else {print $1,$3-1,$3,$7}}' | tee >(gzip > /srv/scratch/surag/scATAC-reprog/mysnap/$tabase.5p.withBarcode.bed.gz)  | sort -k 4 | gzip >  /srv/scratch/surag/scATAC-reprog/mysnap/$tabase.5p.withBarcode.sorted.bed.gz & done`


Note that Snap files are made with 5p ends of reads instead of fragments. This is because SnapTools counts fragments by default, but instead I want to use reads. Command to make Snap files:
`for x in D0 D2 D4 D6 D8 D10 D12 D14 H1 ; do inp=$(ls /srv/scratch/surag/scATAC-reprog/mysnap/${x}_*sorted.bed.gz) ; echo $x ; echo $inp ; snaptools snap-pre --input-file=$inp --output-snap=$x.snap --genome-name=hg38 --genome-size=/users/surag/genomes/hg38/hg38.chrom.sizes --min-flen=0 --max-flen=1000 --keep-chrm=TRUE --verbose=True --min-cov=1000 & done`

Compute bmat:
`for x in D0 D2 D4 D6 D8 D10 D12 D14 H1 ; do snaptools snap-add-bmat --snap-file=$x.snap --bin-size-list 5000 10000 --verbose True & done` 
