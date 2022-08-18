Extract motif PFMs from modisco. By default they would have at least 100 seqlets.
`for i in {1..15} ; do python scripts/modisco_to_pfm.py -m ~/oak/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/chrombpnet/cluster_idx$i//modisco/modisco_results_allChroms_counts.hdf5 -o ./cts$i/ -f 2 & done`

Move into a single PFM file:
`(for x in `ls pfms/cts*/*` ; do printf ">$x\n" ; cat $x ; done) | sed "s/\//_/" > modisco.counts.pfm`

Used GimmeMotifs package v0.15.3--
`gimme cluster modisco.counts.pfm ./gimme_cluster_counts -t 0.999`

Manually inspected clusters. Converted the resulting cluster PFMs to meme format.
`mkdir gimme_cluster_counts/meme`
`python scripts/pfms_to_meme.py -i gimme_cluster_counts/clustered_motifs.pfm gimme_cluster_counts/meme/`

Ran TomTom v5.3.0 to match against Vierstra motif hits.
`mkdir gimme_cluster_counts/tomtom`
`for x in $(ls gimme_cluster_counts/meme/*) ; do (y=$(basename -s ".meme" $x) ; tomtom -no-ssc -oc . -verbosity 1 -text -min-overlap 5 -mi 1 -dist pearson -evalue -thresh 10.0 $x /srv/www/kundaje/surag/resources/motif_archetypes/pfm_meme_format/motifs.meme.txt  > gimme_cluster_counts/tomtom/$y.vierstra.tomtom.tsv) & done`

Inspected matches to Vierstra and chose one with good matches:
`for x in  $(ls gimme_cluster_counts/tomtom/*) ; do cat $x | head -2 | tail -1 ; done | cut -f1,2,5|  sort -k3g | head -36 | cut -f2 > tfs_initial.txt`

Manually made the following changes:
- `SP1_MOUSE.H11MO`: removed it since actual motif (`cts3_pattern_19`) is a weak one 
- `NANOG_MOUSE.H11MO`: removed this as it is nearly identical to PO5F1 (OCTSOX motif), besides it's supposed to be closer to SOX. Clustering mixed up OCT-SOX vs SOX examples and so SOX cluster (`Average_229`) is contaminated with OCT-SOX. Instead added motif that was closest match to `cts11_pattern_4` (using `scripts/pfm_tomtom.py`, manually picked best out of top candidates which was SOX only)
- `SOX15_MA1152.1`: Added, reason above
- `Rfx2.mouse_RFX_2`: Removed, redundant with RFX2
- `REST_HUMAN.H11MO.0.A`: Removed, redundant with REST. Modisco seems to have picked up half motifs.
- `JUN_MA0489.1`: Removed, bad match
- `Gabpa_MA0062.2`: Removed, bad match
- `KLF12_HUMAN.H11MO.0.C`: Removed, bad match
- `Ascl2.mouse_bHLH_1`: Removed, bad motif
- `KLF5_MA0599.1`: Removed. KLF and SP are merged together. Manually added them below.
- `SP2_HUMAN.H11MO.0.A`: Added as closest match to `cts1_pattern_6`.
- `KLF3_HUMAN.H11MO.0.B`: Added as closest match to high OSK KLF (`cts11_pattern_1`)

To get motif hits subseted to peaks (sort throughout till motif names, this can be used to quickly merge files later):
`bedtools intersect -a <(zcat /mnt/data/vierstra_motifs/hg38.all_motifs.v1.0.bed.gz | grep -f tfs_final.txt) -b <(sort -k1,1 -k2,2n ../../20200122_snapATAC/snapATAC_sessions/20210714_n64913/peaks/overlap.peaks.resolved.500.bed) -wa -u -sorted | sort -k1,1 -k2,2n -k3,3n -k4,4 | gzip > motifs.hits.bed.gz` 

Importance thresholding:
`for i in {1..15} ; do (python scripts/importance_thresholding.py -b ~/oak/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/chrombpnet/cluster_idx$i/interpret/bigwig/counts.importance.bw -r ~/oak/projects/scATAC-reprog/bpnet/models/20210820_chrombpnet_lite/chrombpnet/cluster_idx$i/interpret/interpreted_regions.bed -w 2000 -m motif_to_pfm.tsv -s <(bedtools intersect -a  motifs.hits.bed.gz  -b <(cat ~/oak/projects/scATAC-reprog/bpnet/data/20210818_n62599/peaks/overlap_merged/cluster_idx$i.bed | sort -k1,1 -k2,2n ) -wa -u -sorted ) -t 0.99 > importance_thresholded/cluster_idx$i.0.99.bed 2> importance_thresholded/cluster_idx$i.log ) & done`

`sort -m -k1,1 -k2,2n -k3,3n -k4,4 importance_thresholded/cluster_idx*bed | cut -f1-7  | uniq > motifs.importance.thresholded.bed`

Peak x motif matrix for ChromVAR:
`Rscript scripts/make_peak_x_motif_matrix.R`

To extract a representative for each motif cluster, pick constituent motif with the most seqlets:
`grep -f tfs_final.txt <(for x in  $(ls gimme_cluster_counts/tomtom/*) ; do cat $x | head -2 | tail -1 ; done | cut -f1,2,5|  sort -k3g | head -36 | cut -f1-2) > tfs_with_clst.tsv`
`python scripts/get_representative.py --tfs tfs_with_clst.tsv --pfm pfms/ --cluster-key gimme_cluster_counts/cluster_key.txt  -o tfs_final_w_rep.tsv`
`rm tfs_with_clst.tsv`

Added manually for three clusters that were added above.

