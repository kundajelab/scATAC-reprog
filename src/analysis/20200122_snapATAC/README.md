Used script `scripts/make_tagalign_from_bed.sh` to convert to tagaligns suitable for the pipeline (which fails otherwise).
The fragments bed obtained from SnapATAC does not have strand info. Split each fragment into 2 reads of half the length,
with "+" and "-" strands respectively. Pipeline takes tagAlign of reads and fails otherwise.

Ran the pipeline from tagAlign stage (see `scripts/make_jsons.py`) to make the jsons for the pipeline. The ran croo and the outputs are stored on oak and a soft link was made at `./snapATAC_sessions/sesh_name/croo`.

Computed a merged peak set using peaks from bulk + cluster. README for that in `./snapATAC_sessions/20200125_n76770/peaks`. Used this combined peakset as reference and made matrix in `./snapATAC_sessions/20200125_n76770/cluster_bulk_peakset_matrix.` Command for that:
```
bash ./scripts/form_cluster_counts_matrix_from_tagAlign.sh /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_bulk_peakset_matrix/ /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/peaks/bulk.cluster.idr.merged.200.bed 18 /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_tagAligns/cluster_idx /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_bulk_peakset_matrix/cluster.bulk.idr.cluster.counts.txt
```

-------

Command for MACS2 (followed ENCODE ATAC-seq pipeline specs):

```
seq 1 18 | \ xargs -I{} -P10 \
macs2 callpeak -t /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_beds/cluster_idx{}.bed.gz \
-f BED -n /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/macs2/idx{} -g hs -p 0.01 --shift -75 --extsize 150 \
--nomodel -B --SPMR --keep-dup all --call-summits
```

Removed all files but the narrowPeaks.

These files were subsequently removed and not used. Pipeline outputs were used instead.
