Find motif hits that overlap with peaks.

`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/motif_archetypes/hg38.all_motifs.v1.0.bed.gz  | awk '$4=="POU5F1_MA1115.1"') -b ~/kundajelab/scATAC-reprog/src/analysis/20200206_pmat_snapATAC/sessions/20201022_n53906/peaks.bed > POU5F1_MA1115.1.all_peaks.hits`

`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/motif_archetypes/hg38.all_motifs.v1.0.bed.gz  | awk '$4=="SOX2_HUMAN.H11MO.0.A"') -b ~/kundajelab/scATAC-reprog/src/analysis/20200206_pmat_snapATAC/sessions/20201022_n53906/peaks.bed > SOX2_HUMAN.H11MO.0.A.all_peaks.hits`

`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/motif_archetypes/hg38.all_motifs.v1.0.bed.gz  | awk '$4=="KLF4_HUMAN.H11MO.0.A"') -b ~/kundajelab/scATAC-reprog/src/analysis/20200206_pmat_snapATAC/sessions/20201022_n53906/peaks.bed > KLF4_HUMAN.H11MO.0.A.all_peaks.hits`

`bedtools intersect -a <(zcat /srv/www/kundaje/surag/resources/motif_archetypes/hg38.all_motifs.v1.0.bed.gz  | awk '$4=="MYC_HUMAN.H11MO.0.A"') -b ~/kundajelab/scATAC-reprog/src/analysis/20200206_pmat_snapATAC/sessions/20201022_n53906/peaks.bed > MYC_HUMAN.H11MO.0.A.all_peaks.hits`

Cut 6 columns for each for bed
