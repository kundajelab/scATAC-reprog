Info from https://github.com/UcarLab/AMULET/issues/11 on how to make custom singlecell.csv file/
`zcat /srv/scratch/surag/scMultiome-reprog/chromap/barcode_sorted/D2M.frag.bc.sorted.bed.gz  | cut -f4 | usu > D2M/D2M.all.bc.txt`

TSS threshold 6! (pre filtered data has min nFrag 1000)
`cat ~/kundajelab/scATAC-reprog/src/analysis/20220603_Multiome_ArchR/QualityControl/D2M/D2M-Pre-Filter-Metadata.tsv |sed 1d |  awk '$6>6' |  cut -f1 | cut -c5-  > D2M/D2M.cell.bc.txt`

`python make_csv.py -a D2M/D2M.all.bc.txt -c D2M/D2M.cell.bc.txt -o D2M/D2M.csv`

Cuz it needs "tsv.gz" extension:
`ln -s /srv/scratch/surag/scMultiome-reprog/chromap/outputs/D2M.frag.bed.gz  D2M/D2M.frag.tsv.gz`

`bash AMULET.sh /users/surag/kundajelab/scATAC-reprog/src/analysis/20220603_Multiome_AMULET/AMULET/D2M/D2M.frag.tsv.gz /users/surag/kundajelab/scATAC-reprog/src/analysis/20220603_Multiome_AMULET/AMULET/D2M/D2M.csv /users/surag/software/AMULET/human_autosomes.txt /users/surag/kundajelab/scATAC-reprog/resources/blacklist/GRch38_unified_blacklist.bed  /users/surag/kundajelab/scATAC-reprog/src/analysis/20220603_Multiome_AMULET/AMULET/D2M/ /users/surag/software/AMULET/`

Same for D1M.
