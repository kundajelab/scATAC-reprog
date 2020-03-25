Used scripts from surag-scripts/deeptools (commit 735f1c1a).

To make 5p end counts bigwig:
`bash ~/kundajelab/surag-scripts/deeptools/tagaligns_to_cpm_bigwig.sh /users/surag/genomes/hg38/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta.fai /users/surag/kundajelab/scATAC-reprog/src/analysis/20200322_footprinting/20200307_fine_clustering_20200307_gridmap_naive_n15/clusters_20200122_snapATAC_20200125_n76770/bigwigs/cluster14.bw /users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/cluster_tagAligns/cluster_idx14.tagAlign.gz`

Compute matrix:
`bash ~/kundajelab/surag-scripts/deeptools/deepTools_compute_matrix.sh ../beds/MEF2C.homer.intersect.idx15.bed deeoToolsMatrices/MEF2C.homer.intersect.idx15.5p.mat.gz bigwigs/cluster1.bw bigwigs/cluster6.bw bigwigs/cluster7.bw bigwigs/cluster14.bw`

Also performed with heterokaryon samples:
`bash ~/kundajelab/surag-scripts/deeptools/deepTools_compute_matrix.sh ../beds/MEF2C.homer.intersect.idx15.bed deepToolsMatrices/MEF2C.homer.intersect.idx15.with.het.5p.mat.gz bigwigs/cluster1.bw  bigwigs/cluster7.bw  /users/surag/kundajelab/heterokaryon-v2/src/analysis/20191021_surag_AP1_pileup_analysis/bigWigs/5p/batch1.CC.bw /users/surag/kundajelab/heterokaryon-v2/src/analysis/20191021_surag_AP1_pileup_analysis/bigWigs/5p/batch1.16hr.bw`

Scale by flank signal:
`python ~/kundajelab/surag-scripts/deeptools/deepTools_scale_flanks.py -m deepToolsMatrices/MEF2C.homer.intersect.idx15.5p.mat.gz -fb 200 -fe 2000 -o deepToolsMatrices/MEF2C.homer.intersect.idx15.5p.flank.200.2000.norm.4000bp.mat.gz`

Trim:
`python ~/kundajelab/surag-scripts/deeptools/deepTools_trim_matrix.py -m deepToolsMatrices/MEF2C.homer.intersect.idx15.5p.flank.200.2000.norm.4000bp.mat.gz -t 1000 -o deepToolsMatrices/MEF2C.homer.intersect.idx15.5p.flank.200.2000.norm.1000bp.mat.gz`

Plot profile:
`plotProfile -m deepToolsMatrices/MEF2C.homer.intersect.idx15.5p.flank.200.2000.norm.1000bp.mat.gz -o figs/MEF2C.homer.intersect.idx15.5p.flank.200.2000.norm.1000bp.pdf --averageType mean --perGroup --legendLocation upper-right --regionsLabel ""`
