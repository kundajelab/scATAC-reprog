# Transcription factor stoichiometry, motif affinity and syntax regulate single-cell chromatin dynamics during fibroblast reprogramming to pluripotency

This repository contains code for the analysis performed in the paper "Transcription factor stoichiometry, motif affinity and syntax regulate single-cell chromatin dynamics during fibroblast reprogramming to pluripotency" by Nair, Ameen et al. Please refer to the details below for finding the path to the relevant analysis. 

## Important Notes

- As this code as evolved over the course of the project, the figure directories in `src/figures_factory` do not correspond exactly to the figures in the manuscript. Please refer to the index below to find the appropriate notebooks. 
- The cluster IDs used in the repository are different from that in the paper (unless referred to as "`new_cluster`"). Please see `src/figures_factory/configs/cluster.tsv` for the conversion between old cluster IDs to the ones used in the paper.
- The xOSK (extreme OSK) and hOSK (high OSK) states were previously known as hOSK (high OSK) and low OSK states respectively.
- The peak sets are labeled 1-20 in the same order as in the paper.

## Analysis Code

Below, you will find the notebooks listed approximately in the order in which they are run, with their descriptions and commits. 
- The figures can mostly be generated in any order.
- Figures 3, 4, 5, 6 rely on ChromBPNet models.
- The code is a mix of Python and R notebooks. When possible, the `sessionInfo()` is available in the R notebook at the end.
- The analysis directories can be found at `src/analysis`
- Note that SnapATAC requires py2. We used a slightly [modified version](https://github.com/kundajelab/SnapATAC/tree/4cb43f7ef39f02db5ab26e44e314b63e7eef0a3d) of the original repo with minor bugs fixed.
- The figure sections also include code for relevant supplementary figures.

### scATAC-seq Processing

- `20200424_ArchR/MakeArrow.ipynb`: takes fragment files from Chromap as input, makes Arrow files as output. Does basic QC with plots, computes TSS enrichment and doublet scores. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/927ea2491977f80dc5e7cb65bea20ae41e5aaefc/src/analysis/20200424_ArchR/MakeArrow.ipynb)]
- `20200424_ArchR/DoubletAnalysis.ipynb`: Projects doublets on an old UMAP without doublet removal. Determine a threshold by hand tuning. With a final set of thresholds, writes a set of barcodes for each sample that pass QC. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/927ea2491977f80dc5e7cb65bea20ae41e5aaefc/src/analysis/20200424_ArchR/DoubletAnalysis.ipynb)]
- `20200122_snapATAC/snapATAC.ipynb`: Initial scATAC-seq run on 5kb bins. Provides a first UMAP layout and initial clusters, which are manually adjusted. Also outputs fragment files per cluster. TagAligns are created from fragment files, after removing chrM reads. Bulk ATAC-seq pipeline is run on individual clusters to obtain peak calls and signal tracks. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/9f0e519649e2932e468538910792288eabed880a/src/analysis/20200122_snapATAC/snapATAC.ipynb)] [NB: some parts of the notebook were rerun after the version whose outputs were captured]
- Peak resolution script [[commit](https://github.com/kundajelab/scATAC-reprog/tree/a801e8dfadf5054e7a60244ed818103f7dbcb83a/src/analysis/20200122_snapATAC/snapATAC_sessions/20210714_n64913/peaks)]- this is the peak set used for downstream analyses 
- `20200206_pmat_snapATAC/Pmat.ipynb` : Takes peak by cell matrix, filters out cells with few reads in peaks, recomputes UMAP and writes final peak by cell matrix, peaks, UMAP coordinates and clusters. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/01dc2cd648a70623dc0bf6e2072041a85aa4be3e/src/analysis/20200206_pmat_snapATAC/Pmat.ipynb)]
- `20200307_fine_clustering/AssistedFineClustering.ipynb`: Creates peak sets by k-means clustering. Semi-automated step as basic division into 4 categories based on fibroblast/iPSC peaks are enforced. Manual adjustments to clusters also performed later to merge similar clusters and rearrange them. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/ee9eef9bab7f5dc761b5c78e5402d9dc7e09b60f/src/analysis/20200307_fine_clustering/AssistedFineClustering.ipynb)]

### scRNA-seq Processing

- `20200828_RNA_Seurat/QC.ipynb`: Quality control filters based on mitochondrial fraction, number of unique genes, total UMIs and also OSKM fraction. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f96747f3c9b6b39483e706c144d9bd3c6360eb96/src/analysis/20200828_RNA_Seurat/QC.ipynb)]
- `20200828_RNA_Seurat/Seurat.ipynb`: Dimensionality reduction and UMAP for scRNA-seq. Proceeds by first subsampling equal cells from each day, performing scaling and PCA, and then projecting remaining cells using the PCA loadings, followed by a UMAP. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f96747f3c9b6b39483e706c144d9bd3c6360eb96/src/analysis/20200828_RNA_Seurat/Seurat.ipynb)]

### Integration

- `20200828_RNA_Seurat/scATAC_integrate.ipynb`: perform label transfer from ATAC to RNA to get cluster of each RNA cell [[commit](https://github.com/kundajelab/scATAC-reprog/blob/52a39cc9452150858bbb982bb2427c8be6bd3be4/src/analysis/20200828_RNA_Seurat/scATAC_integrate.ipynb)]
- `20200828_RNA_Seurat/scATAC_integrate_CCA.ipynb`: perform RNA → ATAC transfer and get CCA reduction. Default Seurat imputation does not seem to perform well. Instead, performed harmony on CCA reduction to better align ATAC and RNA cells. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/0bd0e8fbc7d9e24a3bba0ff15a04eeaea2133821/src/analysis/20200828_RNA_Seurat/scATAC_integrate_CCA.ipynb)]
- `20200925_Peak2Gene/ArchRIntegrate.ipynb`: peak-gene linking, ATAC→RNA closest cell mapping [[commit](https://github.com/kundajelab/scATAC-reprog/blob/b4c0219b3efea0ef530b34c8d8d797f277b83eb1/src/analysis/20200925_Peak2Gene/ArchRIntegrate.ipynb)]
- [Session files](https://github.com/kundajelab/scATAC-reprog/tree/0bd0e8fbc7d9e24a3bba0ff15a04eeaea2133821/src/analysis/20200828_RNA_Seurat/sessions/20210725_n59378)

### Endogenous vs Sendai Quantification

Quantification relies on the fact that Sendai transcripts end at stop codon whereas endogenous transcripts contain 3' UTR.

- `20211106_sendai_vs_endogenous`: Steps documented in README. For each gene, filter BAM to obtain reads that count towards the gene x count matrix. Use Day 2 pseudo-bulk as all exogenous (Sendai) and iPSC pseudo-bulk as all endogenous. Use 5' end of reads to get read distributions (endogenous vs Sendai). Treat each barcode as being drawn from a mixture model of the two distributions. Used an EM algorithm to estimate per barcode fraction of exogenous transcripts. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/6974ae607a79e6b4bf6dd22d356a2ea4d4a92495/src/analysis/20211106_sendai_vs_endogenous)] [[quantification](https://github.com/kundajelab/scATAC-reprog/blob/6974ae607a79e6b4bf6dd22d356a2ea4d4a92495/src/analysis/20211106_sendai_vs_endogenous/out/quants.tsv)]

### SnMultiome Processing

- `20220603_Multiome_ArchR/MakeArrow.ipynb`:  takes fragment files from Chromap as input, makes Arrow files as output. Does basic QC with plots, computes TSS enrichment. ArchR doublet scores NOT used. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/a23eed75ea1291ac22e64d8a272e96714f4565b9/src/analysis/20220603_Multiome_ArchR/MakeArrow.ipynb)] [[QC](https://github.com/kundajelab/scATAC-reprog/tree/a23eed75ea1291ac22e64d8a272e96714f4565b9/src/analysis/20220603_Multiome_ArchR/QualityControl)]
- `20220603_Multiome_AMULET`: AMULET v1.1 used for doublet detection from ATAC. An additional step was performed by looking at the plot of sorted normalised number of overlaps from the Overlap.txt output and using a manual knee-point detection strategy (see `ProcessAMULET.ipynb`). This gave ~10% more doublets that make intuitive sense. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/d73be6979e53dece246276968625dd23dd33c74c/src/analysis/20220603_Multiome_AMULET)]
- `20220603_Multiome_ArchR/RunArchR.ipynb`: Initial ArchR run on ATAC part of multiome, with and without doublets. Also added scATAC D2 cells to inspect batch effect. Wrote viable barcodes out. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/989b6e7c2a5438aa839e75e2d07ed06803b2fcfb/src/analysis/20220603_Multiome_ArchR/RunArchR.ipynb)] [[Multiome ATAC barcodes](https://github.com/kundajelab/scATAC-reprog/tree/989b6e7c2a5438aa839e75e2d07ed06803b2fcfb/src/analysis/20220603_Multiome_ArchR/barcodes/20220607_TSS6_nFrag1000_AMULET)]
- `20220606_Multiome_RNA_Seurat/QC.ipynb`: Quality control filters based on mitochondrial fraction, number of unique genes, total UMIs and also OSKM fraction. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/42f0568bbfdd2546e886ab049ab308ae13f10ddb/src/analysis/20220606_Multiome_RNA_Seurat/QC.ipynb)]
- `20220609_Multiome_SnapATAC/snapATAC.ipynb`: D2 scATAC + Multiome ATAC-seq run on 5kb bins. Filtered D2 scATAC to only those cells in top 5 clusters by count (for D2). Provides an initial UMAP layout. Ran Harmony to remove batch effects between scATAC and Multiome ATAC. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4aa04ca0342b9e9b7aeeca295517c5d8da8b6698/src/analysis/20220609_Multiome_SnapATAC/snapATAC.ipynb)]
- `20220606_Multiome_RNA_Seurat/Seurat.ipynb`: Dimensionality reduction and UMAP for scRNA-seq. Doublet detection using DoubletFinder as for scRNA-seq.  some cells with OSKM expression clustered together in RNA-seq in one corner — most of them did not pass ATAC QC. Use OSKM% < 0.5 as a filter since this is single nucleus and shouldn’t expect much/any Sendai transcripts. Wrote final set of barcodes after intersecting with ATAC viable barcodes. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/42f0568bbfdd2546e886ab049ab308ae13f10ddb/src/analysis/20220606_Multiome_RNA_Seurat/Seurat.ipynb)] [[barcodes](https://github.com/kundajelab/scATAC-reprog/tree/master/src/analysis/20220606_Multiome_RNA_Seurat/barcodes/20220607_nFeat200_mt15_oskm0.5_nCount2000_doub15_pk0.01_atac_filt)]
- `20220609_Multiome_SnapATAC/snapATAC_make_pmat.ipynb`: Made peaks x barcode matrix for D2 scATAC + Multiome ATAC-seq data, using previous set of peaks. [NB: this requires `add-pmat` step in snapTools] [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4aa04ca0342b9e9b7aeeca295517c5d8da8b6698/src/analysis/20220609_Multiome_SnapATAC/snapATAC_make_pmat.ipynb)]
- `20220611_Multiome_Label_Transfer/ATAC_Multiome_label_transfer.ipynb`: Transferred labels from scATAC → Multiome using Seurat FindTransferAnchors on Harmony embeddings. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/e95581e52596ce6eb07723c9299f5374e4177fc7/src/analysis/20220611_Multiome_Label_Transfer/ATAC_Multiome_label_transfer.ipynb)]

### Fig 1

- `UMAP_stats.ipynb`: UMAP + sample x cluster breakdown plots [[commit](https://github.com/kundajelab/scATAC-reprog/blob/03ac53c214b39ed193895433634f7d591442880b/src/figures_factory/Fig1/UMAP_stats.ipynb)]
- `FRiP.ipynb`: For every ATAC cell, compute fraction of reads in fibroblast peaks and in iPSC and naive/primed ESC peaks [[commit](https://github.com/kundajelab/scATAC-reprog/blob/cf6312270a611e7031d0e6cb8076a83d37358e39/src/figures_factory/FRiP.ipynb)]
- `GeneSetExpr.ipynb`: Averaged per scRNA cell expression z-score for 84 fibroblast genes and 20 pluripotency associated genes [[commit](https://github.com/kundajelab/scATAC-reprog/blob/70e8a20f4ae515ee458a571d1ef4892e5d98c2a8/src/figures_factory/GeneSetExpr.ipynb)]. Original [lists](https://github.com/kundajelab/scATAC-reprog/tree/70e8a20f4ae515ee458a571d1ef4892e5d98c2a8/src/analysis/20200828_RNA_Seurat/lists) of genes. Subset of these genes that were present in the counts matrix were used (originally 88 and 22).
- `GenomeShots.ipynb`: Gene browser shots of specific gene loci along with expression for every cluster [[commit](https://github.com/kundajelab/scATAC-reprog/blob/14ddad7f924e3a5a2c6fed7aa29864eb84860422/src/figures_factory/GenomeShots.ipynb)]
- `GeneScores.ipynb`: ATAC derived gene scores for every single cell. Uses ArchR's computed gene scores and smooths it [[commit](https://github.com/kundajelab/scATAC-reprog/blob/14ddad7f924e3a5a2c6fed7aa29864eb84860422/src/figures_factory/GeneScores.ipynb)]
- `ExprPlots.ipynb`: scRNA expression plots. Added endogenous/exogenous OSKM plots. Also OAS[1-3,L], DPPA2/3/5, DNMT3L for extended fig. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/9db0c07613cb49b3d978062b75fa4ac452407d2d/src/figures_factory/ExprPlots.ipynb)]
- `TerminalExpressionMatrix.ipynb`: For a few "terminal" states plot the single-cell matrix of cell state specific gene expression. The gene sets were picked manually from above clustering. Equal number of barcode sampled for each cell state. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f95dffa0451c6ba324b014232de63ea66ede0d57/src/figures_factory/Fig2/TerminalExpressionMatrix.ipynb)]

- Trajectory:    
    - `analysis/20200217_trajectory/Paga.ipynb`: PAGA analysis for scATAC cells. Uses diffusion map top 10 components. Computes pseudotime— once using fibroblast cells as root and other time using xOSK cells as root. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4995481863f9d32939ebd91a762b3ef0b4be0978/src/analysis/20200217_trajectory/Paga.ipynb)] [[outputs](https://github.com/kundajelab/scATAC-reprog/tree/4995481863f9d32939ebd91a762b3ef0b4be0978/src/analysis/20200217_trajectory/sessions/20211003_n62599)]
    - `PAGA_connectivities.ipynb`: Plot the PAGA graph [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4995481863f9d32939ebd91a762b3ef0b4be0978/src/figures_factory/Fig2/PAGA_connectivities.ipynb)]
    - `TrajectoryArrows.ipynb`: plot trajectory arrows for main trajectories [[commit](https://github.com/kundajelab/scATAC-reprog/blob/0aab301a706e524393ed5ae2723e9e45f94429da/src/figures_factory/Fig2/TrajectoryArrows.ipynb)]

_Supplement_
- `Fig1/Supp.ipynb`: CCA plots, transfer scores histogram and transfer scores correlation [[commit](https://github.com/kundajelab/scATAC-reprog/blob/87521af5fd30a3fe5aa82b55a926f83d16647c03/src/figures_factory/Fig1/Supp.ipynb)]
- `20230612_OSKM_expr_field/OSKVectorField.ipynb`: vector field based on sendai expression of OSKM. Suggests cells “fall off” primary reprogramming trajectory into partially reprogrammed state. Discretised UMAP into grid, and computed “speed” based on difference in total sendai expression of adjacent bins. Removed regions with low sendai expression. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/b7a39c318a97afbdaf5abcbe534c60a16780f951/src/analysis/20230612_OSKM_expr_field/OSKVectorField.ipynb)]
    - This has been **superseded** by `20230612_OSKM_expr_field/OSKVectorField_knn.ipynb`. We first find the 14 nearest neighbors of a cell (excluding itself). For each cell and each neighbor, we look at the difference vector between their coordinates in UMAP space. We normalize this and weight be difference in expression between the two points. Finally we compute an average direction for each cell. Beyond this, we discretised the UMAP and followed steps similar to `OSKVectorField.ipynb`. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4e38a9eaa123/src/analysis/20230612_OSKM_expr_field/OSKVectorField_knn.ipynb)]
- `PseudotimePlots.ipynb`: Plot pseudotime on UMAPs [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f6c20aaf67d0ba37205d7da150677b8a6bdfbd00/src/figures_factory/Fig2/PseudotimePlots.ipynb)]

### Fig 2

[[pdfs](https://github.com/kundajelab/scATAC-reprog/tree/a9403e5bc1a30226a645ae8170c30632f1ae2687/src/figures_factory/Fig2/subfigs)]

- Expression and ChromVAR:
    - `analysis/20200522_OSK_frip/OSKM_ChromVAR.ipynb`: running ChromVAR using JASPAR/HOCOMOCO TF motifs for OSKM [[commit](https://github.com/kundajelab/scATAC-reprog/blob/5a8b4fa00c2d090601854313b94aea4193bfa676/src/analysis/20200522_OSK_frip/OSKM_ChromVAR.ipynb)] [[outputs](https://github.com/kundajelab/scATAC-reprog/blob/5a8b4fa00c2d090601854313b94aea4193bfa676/src/analysis/20200522_OSK_frip/sessions/20210717_n62599/OSKM_ChromVAR.tsv)]
    - `analysis/20200522_OSK_frip/data/pfms/`: PFMs used for ChromVAR [[pfms](https://github.com/kundajelab/scATAC-reprog/tree/88ab7da5c174b46f28d841e091d95613bfd5fe5d/src/analysis/20200522_OSK_frip/data/pfms)]
    - `OSKM_ChromVAR_plot.ipynb`: ChromVAR plots + per cell state box-plots. For box-plots, ChromVAR deviations are min-max normalised per motif to 0.1-0.95 quantiles [[commit](https://github.com/kundajelab/scATAC-reprog/blob/88ab7da5c174b46f28d841e091d95613bfd5fe5d/src/figures_factory/Fig2/OSKM_ChromVAR_plot.ipynb)]
    - `figures_factory/ExprPlots.ipynb`: Expression plots per gene [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4b75ba985e3cc199aac2c264b8a183ebf4797ee1/src/figures_factory/ExprPlots.ipynb)]
    - `Expr_ChromVAR_collate.ipynb`: collate expression and ChromVAR plots [[commit](https://github.com/kundajelab/scATAC-reprog/blob/57b981a0c3fd85f2f49e5435d52c4ebe45f5d031/src/figures_factory/Fig2/Expr_ChromVAR_collate.ipynb)]   
- `OSKM_States.ipynb`: k-means based on OSKM expression only [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3bf9bdda6b74fb48d5b90c0e69a52af45be67195/src/figures_factory/Fig2/OSKM_States.ipynb)]

_Supplement_
- `Per_state_expr.ipynb`: Per cell state normalised expression box-plots. For box-plots, log expressions are min-max normalised per gene to 0-0.99 quantiles [[commit](https://github.com/kundajelab/scATAC-reprog/blob/45ee710e06868f6d19ce9e503bfc20cf62f45bf4/src/figures_factory/Fig2/Per_state_expr.ipynb)]
- `OSKM_per_state_per_day_expr.ipynb`: Median cell OSKM endogenous/exogenous TPM by day x cell state. Retained day x cell state combinations with >50 cells. Note exogenous median is computed from median total - median endogenous. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/35f431e9210e99eef77cf6e11cd53e4ac417a1a2/src/figures_factory/Fig2/OSKM_per_state_per_day_expr.ipynb)]
- `OSKM_Corr_ChromVAR_Expr.ipynb`: Expression and ChromVAR correlation for across matched ATAC-RNA cells [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f6df1531820dbcb9b718f64492bc759ab79ecd2e/src/figures_factory/Fig2/OSKM_Corr_ChromVAR_Expr.ipynb)]
- Gene sets:
    - `analysis/20200828_RNA_Seurat/FineClustering.ipynb`: Top 5000 variable genes as per `FindVariableFeatures`, with at least 50 transcripts across all cells — total 4306 cells. Perform k-means clustering on genes. Perform GO enrichment on peak sets (gprofiler2 version `e104_eg51_p15_3922dba`) [[commit](https://github.com/kundajelab/scATAC-reprog/blob/e7d7afbef52028103ae0588805d1939daff59d46/src/analysis/20200828_RNA_Seurat/FineClustering.ipynb)]  [[gene sets and GO](https://github.com/kundajelab/scATAC-reprog/tree/8ec75d467b3ca5249273059f864f7c2a0becc1a9/src/analysis/20200828_RNA_Seurat/gprof_results/20211005_n59378)]


### ChromBPNet Models

The code used for model training, evaluation and interpretation is available at `src/chrombpnet`. However, if you are interested in training ChromBPNet models, it is recommended to use the up-to-date full feature version at [https://github.com/kundajelab/chrombpnet](https://github.com/kundajelab/chrombpnet). 
- Scripts used: `20200626_modeling_runs/chrombpnet-lite/jobscripts` jobscripts for all folds [[commit](https://github.com/kundajelab/scATAC-reprog/tree/3bbb0e46acf5332ac6061b35916a398738745acc/src/analysis/20200626_modeling_runs/chrombpnet-lite)]

### Motifs

- Workflow described in README. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/master/src/analysis/20211007_motif_consolidation/20210820_chrombpnet_lite)]

**Curation:**

- extract modisco counts motifs PFMs (adding profile gives the same, so instead stuck with counts only). Ignored negative motifs for now.
- Cluster using GimmeMotifs' `gimme cluster` command
- Match the clustered motifs with hits from Vierstra's list of motifs using TomTom
- Manually curate the list to include/exclude TFs (`tfs_final.txt`)
- Added representative motif for each cluster by choosing the constituent motif (across clusters) with the highest number of seqlets [[commit](https://github.com/kundajelab/scATAC-reprog/tree/master/src/analysis/20211007_motif_consolidation/20210820_chrombpnet_lite)] (`tfs_final_w_rep.txt`)
- Added names for clusters and put in a [[meme file](https://github.com/kundajelab/scATAC-reprog/blob/e0d76b39ab8a9f8a5080ea81a739226a56d66f4e/src/analysis/20211007_motif_consolidation/20210820_chrombpnet_lite/tfs_final_w_rep.meme)]
- Mapped all motifs back to curated motifs using TomTom (`20230607_re_modisco_breakdown`). Manually resolved minor discrepancies. Mostly re-labeled motifs that were dimers of the 30 curated motifs (using MOTIFA:MOTIFB format). Use a q-value cutoff of 0.05. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/e0d76b39ab8a9f8a5080ea81a739226a56d66f4e/src/analysis/20230607_re_modisco_breakdown)] [[annotated_motifs](https://github.com/kundajelab/scATAC-reprog/tree/e0d76b39ab8a9f8a5080ea81a739226a56d66f4e/src/analysis/20230607_re_modisco_breakdown/manually_adjusted)]
- `Misc/modisco/Supp_cell_state_x_motif.ipynb`: Plotting fraction of seqlets of each motif (out of all seqlets for that cell state's modisco, transformed to log10 scale) for 30 main motifs (no dimers). Note that KLF and SP seem exclusive, because the motifs are very similar and assignment is made to only one of them. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/0de90ea58693b0aeec3aa50b59209f58d27c4dfa/src/figures_factory/Misc/modisco/Supp_cell_state_x_motif.ipynb)]

**Scanning:**

- subset Vierstra motif hits to peaks and to selected TFs
- Use [importance thresholding](https://github.com/kundajelab/scATAC-reprog/blob/70a737a2c8b1666e399f31e71e9ba992bd382ffe/src/analysis/20211007_motif_consolidation/20210820_chrombpnet_lite/scripts/importance_thresholding.py) to reduce to important hits. This works by creating a null distribution of importance scores given a motif by computing summed absolute importance score (weighted by "silhouette" of motif, i.e. it's max IC score per position)  and then thresholding to top 0.99 of this
- Creating a matrix of peak x motif
- `20200607_ChromVar/ChromVAR.ipynb`: ran ChromVAR on peak x motif matrix [[commit](https://github.com/kundajelab/scATAC-reprog/blob/63d91e5e4f75e84187df2b70bd91e64bc720e371/src/analysis/20200607_ChromVAR/ChromVAR.ipynb)]

### Footprinting

- `Supp_Vignette_CTCF_footprint_py.ipynb` and `Supp_Vignette_CTCF_footprint_R.ipynb`: Vignette with bias model prediction, per state w/ and w/o bias preds , importances at a CTCF motif [[commit](https://github.com/kundajelab/scATAC-reprog/blob/bcbe7ab4474fa2ddd0139e31f784b84af17c20b4/src/figures_factory/Fig5/Supp_Vignette_CTCF_footprint_py.ipynb)]
- `Fig5/Aff_vs_conc_footprints_all_TFs.ipynb`: Footprinting of all TFs for all cell states. Uses the representative version for each of the 30 curated motifs and splits seqlets  into 3 bins (low: quantiles 0.1-0.4, medium 0.4-0.7, high 0.7-1). Introduces seqlets into random negative regions for each cell type. Seqlets may be repeated till at least 1000 total sequences are scored. These are stored in extended figure, and a subset of those are in the supplements (filtered and edited in Illustrator).  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/master/src/figures_factory/Fig5/Aff_vs_conc_footprints_all_TFs.ipynb)] [[corresponding PWMs](https://github.com/kundajelab/scATAC-reprog/blob/9d31f197215f5de2be427a12150424c73a0ae199/src/figures_factory/Fig5/Aff_vs_conc_footprints_all_TFs_PWMs.ipynb)]

- `Supp/ModelFreeFootprints.ipynb`: Generates footprints by aggregating insertions. Uses MoDISco PWMs (xOSK KLF, OCTSOX; Fibroblast AP1). Performed PWM scanning. Split into log-odds bins ( these bins are slightly different from those used above since it was done before the all motifs x all cell state footprinting). After getting an example's 2000 bp counts matrix (per cell state, bin pair) centered at motifs after accounting for orientation, row normalized the matrix and then averaged across columns to generate footprint [**NB**: motifs PWMs come from `Aff_vs_conc_footprints.ipynb`, which was later not used] [[commit](https://github.com/kundajelab/scATAC-reprog/blob/d6dc72b6a9e2c753168c9948c5fe605225107652/src/figures_factory/Fig5/Supp/ModelFreeFootprints.ipynb)] [[processing](https://github.com/kundajelab/scATAC-reprog/tree/d6dc72b6a9e2c753168c9948c5fe605225107652/src/figures_factory/Fig5/Supp/model_free_footprints)]

### Fig 3

- `LocusExploreShot.ipynb`: NANOG locus with expression plots. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/98193925c26fd1e6c4795be5792f4daa9cba16db/src/figures_factory/LocusExploreShot.ipynb)]
- `figures_factory/LocusImportanceScores.ipynb`: See Fig4
- `PerGeneEnhTF.ipynb`: TF-enhancer links for genes of interest (”TF2G plot”). Plots dynamic enhancer-TF connections over cell states using correlated peaks of gene of interest. Involves manual interventions: SOX motifs overlapping with OCTSOX are removed, TFAP2 overlapping with KLF are removed, KLF overlapping with CTCF are removed. Motifs are turned off in the cell states in which they are not recovered by TF-MoDISco. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/988b59dc25311427a91e3d6ae886ce6c0ccc235c/src/figures_factory/Fig6/PerGeneEnhTF.ipynb)]
    - **NB**: Assumes that importance scores are only computed in peaks of a given sample. Therefore enhancers that are closed in a cell state will not have any links.
- `MicroC.ipynb`: Plotting 4DN MicroC data from fibroblasts and hESC at NANOG locus [[commit](https://github.com/kundajelab/scATAC-reprog/blob/7e89e2a9a35cc82e2544458c653fb10b2ece9e08/src/figures_factory/Fig6/MicroC.ipynb)]
- `MoDISco_Breakdown_Plot.ipynb`: Builds on `20211118_modisco_breakdown`. Curate top motifs across cell types, assign MoDISco motifs to them using TomTom followed by manual adjustments. Plots breakdown of seqlets per cell state to these top motifs. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/1fbb44628d660497c19b7915a19e1e89e8fa2c74/src/figures_factory/Fig4_new/MoDISco_Breakdown_Plot.ipynb)] [[preprocessing](https://github.com/kundajelab/scATAC-reprog/tree/5556a9f5fc7f6e52c106f431718abe48302513c4/src/analysis/20211118_modisco_breakdown)]
    - **NB**: For some reason I used a different set of curated motifs instead of the 30 in `tfs_final.txt`
    - **This has been superseded by** `20230607_re_modisco_breakdown` [[commit]](https://github.com/kundajelab/scATAC-reprog/tree/ee1c8e247dc8a/src/analysis/20230607_re_modisco_breakdown).  Updated plot can be found in `MoDISco_Re_Breakdown_Plot.ipynb` [[commit]](https://github.com/kundajelab/scATAC-reprog/blob/ee1c8e247dc/src/figures_factory/Fig4_new/MoDISco_Re_Breakdown_Plot.ipynb)
    - **This has been further superseded by** `MoDISco_Re_Breakdown_Hits_Plot.ipynb`. In this, we use the motif hits, filter them down to motifs picked up by MoDISco in each cell type, and handle SP and KLF manually since their sites tend to overlap a lot. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3aab1897170/src/figures_factory/Fig4_new/MoDISco_Re_Breakdown_Hits_Plot.ipynb)]


_Supplement_
- `Misc/performance/ChromBPNet_performance.ipynb` : Plot counts and profile performance of ChromBPNet models for all folds. Includes plot of read depth of each sample, and best bound for profile performance based on pseudo reps (see below) [[commit](https://github.com/kundajelab/scATAC-reprog/blob/552d4839fcf6fa5c4e4ca976b58b558032fbda0d/src/figures_factory/Misc/performance/ChromBPNet_performance.ipynb)]
- `Misc/performance/Pseudorep_JSD.ipynb` : Compute JSD of pseudo reps. First considered a strategy of splitting per base counts into 2 exclusive pseudo reps, but the performance of this doesn't seem very good. Instead, take 2 independent pseudo reps (with half the reads of the original sample) and compute JSD [[commit](https://github.com/kundajelab/scATAC-reprog/blob/552d4839fcf6fa5c4e4ca976b58b558032fbda0d/src/figures_factory/Misc/performance/Pseudorep_JSD.ipynb)]

### Fig 4

- `figures_factory/Fig4_new`
- `Py_Vignette` and `R_Vignette` for LEFTY1 enhancer region and CDH1 promoter analyses. Includes in-silico motif mutagenesis for CDH1 promoter.
- `Py_Vignette.ipynb` and `R_Vignette.ipynb`: Importance score vignette for selected regions [[commit](https://github.com/kundajelab/scATAC-reprog/blob/5f7ec276b3d1ee8078115db852f1a5c3636ee08d/src/figures_factory/Fig3/R_Vignette.ipynb)]. Computes and plots for all cell types irrespective of peak status.
- `PeaksToGene.ipynb`: Heatmaps of peak set x cell state, linked gene sets x cell stat, as well as a grid based UMAP plot of per peak set accessibility [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f11f39ae1af3ffcf8cce8dd3a907e40b93d01afd/src/figures_factory/Fig3/PeaksToGene.ipynb)]
- `CurateGo.ipynb`: GO enrichment using gProf for every gene set linked to peaks in every peak set. Used version `e104_eg51_p15_3922dba` of gProf. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f11f39ae1af3ffcf8cce8dd3a907e40b93d01afd/src/figures_factory/Fig3/CurateGO.ipynb)]
- `BPNetHitsPeakSetMotifs.ipynb`: Counted motifs per peak set, normalised them and plotted a matrix  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3f3a0b938f6865a7f7f93adb650d4e2ffd4b70bf/src/figures_factory/Fig3/BPNetHitsPeakSetMotifs.ipynb)]


_Supplement_
- `FineClusteringSuppFig.ipynb`: Fine clusters used for peak clustering [[commit](https://github.com/kundajelab/scATAC-reprog/blob/5aeddd680f5dbbec277879b11ed88d55e1e60a9b/src/figures_factory/Fig2/FineClusteringSuppFig.ipynb)]
- `MotifExpressionHeatmap.ipynb`: For main pseudotime trajectory, plot ChromVAR score + expression of correlated TFs [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3f3a0b938f6865a7f7f93adb650d4e2ffd4b70bf/src/figures_factory/Fig3/MotifExpressionHeatmap.ipynb)]
- `GenePseudotime.ipynb`: For selected TFs, plot ChromVAR score, expression and gene activity score (ArchR derived) along main trajectory pseudotime [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3f3a0b938f6865a7f7f93adb650d4e2ffd4b70bf/src/figures_factory/Fig3/GenePseudotime.ipynb)]
- For Venn diagram, merged overlap peaks for each cell state and computed intersection count using bedtools intersect (-wa -u)
  
_Related_
- `20200514_Homer_summary_plot_factory/HomerSummary.ipynb`: Summarised HOMER knownMotif runs on all peak sets in the style of Knaupp et al 2017. Manually selected matching HOMER motifs matching the TF list (JASPAR/HOCOMOCO) used for other analyses  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/3b495df2dda61fed56b5a9339ac6efe64a0d9780/src/analysis/20200514_Homer_summary_plot_factory/HomerSummary.ipynb)] [[directory](https://github.com/kundajelab/scATAC-reprog/tree/3b495df2dda61fed56b5a9339ac6efe64a0d9780/src/analysis/20200514_Homer_summary_plot_factory)]

### Fig 5

- `dhs_overlap.sh` and `DHS_overlap.ipynb` [[dhs_overlap.sh](https://github.com/kundajelab/scATAC-reprog/blob/dc696746653a1f6d552721dc3761524075e9716e/src/figures_factory/Fig5/dhs_overlap.sh), [DHS_overlap.ipynb](https://github.com/kundajelab/scATAC-reprog/blob/dc696746653a1f6d552721dc3761524075e9716e/src/figures_factory/Fig5/DHS_overlap.ipynb)] Compute overlap of peak sets with peaks from DNase Index
- `make_early_on_peak_set.sh`: set of peaks that is not in peak sets 6,7,8 or fibroblast peaks but is open along all other cell states along the primary reprogramming trajectory [[script](https://github.com/kundajelab/scATAC-reprog/blob/0665a0386a192a1bb1b5befb3eb4703ea9c95b75/src/figures_factory/Fig5/make_early_on_peak_set.sh)]
- `VortexPlots.ipynb`: Vortex plots with integrative analysis of bulk TF and histone ChIP-seq datasets [[commit](https://github.com/kundajelab/scATAC-reprog/blob/050e33b5ddd89f4ea979c4be3a63a531dc440d3f/src/figures_factory/Fig5/VortexPlots.ipynb)]

- `high_OSK_vs_iPSC_modisco.ipynb` compares OCT-SOX motifs between xOSK and iPSC states. Manually removes a subcluster of OCT-SOX in iPSC which resembled OCT-only motif. Computes log odds scores of instances [[notebook](https://github.com/kundajelab/scATAC-reprog/blob/e93067f761eb415d772a82bddb4d714dbd732105/src/figures_factory/Fig5/high_OSK_vs_iPSC_modisco.ipynb)]. Plots heatmap of instances. Exports aggregate PWM, CWM, and per subcluster PWM.  `OS_motifs.ipynb` plots the aggregate PWM and CWM, and per subcluster PWMs [[notebook](https://github.com/kundajelab/scATAC-reprog/blob/e93067f761eb415d772a82bddb4d714dbd732105/src/figures_factory/Fig5/OS_motifs.ipynb)].
- `high_OSK_vs_iPSC_modisco_BPNet_logodds.ipynb` same as above, but computes log odds scores of instances using the BPNet OCTSOX motif [[notebook](https://github.com/kundajelab/scATAC-reprog/blob/db1aa046a17ffa07cfa00a5443e981d125c59d96/src/figures_factory/Fig5/high_OSK_vs_iPSC_modisco_BPNet_logodds.ipynb)]

- `FindThreshold.ipynb`: Using the BPNet derived motif for OSK and HOMER motif for AP1 (GSE21512). Compute log-odds thresholds for canonical OSK and AP1 motifs by scoring xOSK state seqlets and taking 10th percentile of scores as threshold. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/e07e84a9978871fd9024bbe1c9600bcffb729891/src/figures_factory/Fig5/FindThreshold.ipynb)]
- `MotifScanImportanceThreshold.ipynb`: Threshold PWM called motifs by importance scores. Uses xOSK state importance score. Note that not all peaks in peak sets 6,7,8 are also peaks for xOSK, and so hits falling in those are eliminated in this analysis, i.e. only peaks within xOSK state are considered. [[notebook](https://github.com/kundajelab/scATAC-reprog/blob/e07e84a9978871fd9024bbe1c9600bcffb729891/src/figures_factory/Fig5/MotifScanImportanceThreshold.ipynb)] [[scan_output](https://github.com/kundajelab/scATAC-reprog/tree/e07e84a9978871fd9024bbe1c9600bcffb729891/src/figures_factory/Fig5/motif_scans)]
- `Peak_set_x_affinity.ipynb`: Bar plots of affinity for OSK + AP1 in early transient peak sets [[commit](https://github.com/kundajelab/scATAC-reprog/blob/e1277064bcaf0db02c7a34f8c4ddee126565780d/src/figures_factory/Fig5/Peak_set_x_affinity.ipynb)]

- `/oak/stanford/groups/akundaje/surag/projects/scATAC-reprog/clusters/20210714_n64913/extra/D2_c11/`: Subsample of xOSK cluster with Day 2 cells only, with fragment file and bulk pipeline output.

- `ChromVAR_affinity.ipynb`: pseudo-binding saturation curves. Stratified newly opened peaks at day 2 (based on peaks called on xOSK cells subsetted to day 2 only) based on affinity of OCTSOX motif present, into 3 bins (low, medium, high). Assigned label corresponding to strongest motif in a peak. Ran ChromVAR on those peak sets and min-max normalized the scores. Repeated analysis for KLF.  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/2b07b9f32044fe2cf89d22d4a8fcd5922487e8b2/src/figures_factory/Fig5/ChromVAR_affinity.ipynb)]
- `ChromVAR_affinity_expr_companion.ipynb`: Per cluster log expression for OSK. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/2b07b9f32044fe2cf89d22d4a8fcd5922487e8b2/src/figures_factory/Fig5/ChromVAR_affinity_expr_companion.ipynb)]

_Supplement_
- `VortextPlotsESC.ipynb`: Plot with GSE101074 integration. Plotted fibroblast, pre-iPSC and iPSC signal at naive and primed specific ESC peaks borrowed from GSE101074. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/f11f39ae1af3ffcf8cce8dd3a907e40b93d01afd/src/figures_factory/Fig3/VortexPlotsESC.ipynb)]

_Related_
- `Supp/SuppVortexPlots.ipynb`: H3K27ac plot for early transient + E-ON peaks [[commit](https://github.com/kundajelab/scATAC-reprog/blob/34eb0cf573f24cf44b5839471a11c43bda8b9abf/src/figures_factory/Fig5/Supp/SuppVortexPlots.ipynb)]

### Fig 6 (Multiome)

- `UMAP_stats.ipynb`: UMAPs [[commit](https://github.com/kundajelab/scATAC-reprog/blob/62cef6a09464a747650ecdf09fed222b3912f8ab/src/figures_factory/Multiome/UMAP_stats.ipynb)]
- `FibrExpr.ipynb`: Expression of fibroblast-specific genes in different multiome clusters. Gene set used came from differential genes between fibroblast and iPSC from scRNA-seq. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/1c3c4f2a427cd196e6c6b4ab894e1dad7689dbca/src/figures_factory/Multiome/FibrExpr.ipynb)] [[notebook for diff gene calling](https://github.com/kundajelab/scATAC-reprog/blob/1c3c4f2a427cd196e6c6b4ab894e1dad7689dbca/src/analysis/20220612_Multiome_Repression/scRNA_fibr_diff.ipynb)] [[diff genes](https://github.com/kundajelab/scATAC-reprog/blob/1c3c4f2a427cd196e6c6b4ab894e1dad7689dbca/src/analysis/20220612_Multiome_Repression/fibr_ipsc_diff.txt)]
- `PileupPlots.ipynb`: Plot of signal in different cell types and peak sets from D1M and D2M. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/15c2dba107e5428cb9e4a31eac78008d88312ed7/src/figures_factory/Multiome/PileupPlots.ipynb)]
- `AP1_transient_Footprint.ipynb`: Generate aggregate footprints of AP1 at transient sites. Use bias model to get an aggregate null and use that for  correction. See README for how regions were generated. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/be406d491dd078cbefe07124ad6965c3f84d6d7e/src/figures_factory/Multiome/AP1_transient_Footprint.ipynb)] [[README](https://github.com/kundajelab/scATAC-reprog/tree/be406d491dd078cbefe07124ad6965c3f84d6d7e/src/figures_factory/Multiome)]
- `AP1_transient_Footprint_scATAC.ipynb`: Same as `AP1_transient_Footprint.ipynb` but using scATAC-seq xOSK and fibroblast data + model.  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/1bc0851682b76b235d76cca69e0b80d583467c03/src/figures_factory/Multiome/AP1_transient_Footprint_scATAC.ipynb)]
- `TransAP1vsFibrExpr.ipynb`: AP1 sequestration/retention plots plotting fraction of reads in transient/existing peaks with AP1 motifs and fibroblast-specific gene expression. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/b9b6ee8c141b232a35405d801deebc065740aca3/src/figures_factory/Multiome/TransAP1vsFibrExpr.ipynb)]
- `README`: code for how stats were derived for the text [[README](https://github.com/kundajelab/scATAC-reprog/blob/5ab99012537bd798cd59ca25fbe6c8906d4c815a/src/figures_factory/Multiome/README.txt)]:
    - AP1 peaks overlapping fibroblast peaks and xOSK peaks that are not fibroblast peaks
    - xOSK non fibroblast AP1 instances that overlap with early transient peak sets
    - fibroblast-specific AP1 instances that are closed early during reprogramming. Overall xOSK seems to have fewer peaks called, so to get a conservative estimate (i.e. underestimate how many peaks are closed), we considered fibroblast specific AP1 instances in peaks that are not open in both xOSK and Intermediate (C11) states.
    - note that the hit calling (motif and thresholding) for fibroblast-specific AP1 and xOSK specific AP1 are different. However, using the same one (e.g. from `motifs.importance.thresholded.bed` results in slightly more xOSK-specific hits. The current approach is thus conservative (i.e. underestimating new non-fibroblast AP1 sites). So for consistency with other plots (footprint, sequestration plots etc) it has been left as is.
    
_Supplement_
- `D2_Mixing.ipynb`: Shows how nearest neighbors cross modality (scATAC vs multiome snATAC) change post Harmony  [[commit](https://github.com/kundajelab/scATAC-reprog/blob/61d46aea396b907f5de1672a2606758032459b2c/src/figures_factory/Multiome/D2_Mixing.ipynb)]

### Misc

- `20230213_design_AP1_sink_vectors`: Simple method to generate AP1 sink vector. Extract genomic instances of AP1 with flank sequence (21bp total). Stitch together and scan for matches to known relevant motifs (using HOMER). Manually edit the sequences to remove non-AP1 matches. Replace AP1 with either `CCCAAACCC` or  `GGGTTTGGG`, as scrambling AP1 created sites for OCT or FOX. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/master/src/analysis/20230213_design_AP1_sink_vectors)]

## Export

Code used to streamline/organize files to be exported and exposed.

- `20230814_exports/models/models_mtbatchgen.ipynb` and `20230814_exports/models/models_tf2.ipynb`: renamed and saved files using the `mtbatchgen` env (py3.7, tf 1.14) to  `out/` dir. Re-created models in `tf2` env (py3.10, tf 2.8) and loaded weights, and saved in SavedModel format. Also saved the weights. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/a6658c639aaa06aea7d09029d2876ab5065888ca/src/analysis/20230814_exports/models)]
- `20230814_exports/scATAC_data.ipynb`: Export cell and peak data. Replaced with new cluster IDs and attached peak set labels to peaks. Note that ~5k peaks are not assigned to any set because of low reads/variance in peak set curation that was performed earlier [[commit](https://github.com/kundajelab/scATAC-reprog/blob/4e220fa1feb0ef8775d7eeb10c797dcd68124643/src/analysis/20230814_exports/scATAC_data.ipynb)]
- `20230814_exports/scRNA_data.ipynb`: Export Seurat object after removing unnecessary metadata and adding in cluster labels. Also stored raw counts matrix (matrix market format), genes, cell metadata, and PCA coordinates separately. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/c5eb673c9f627bf153ab474f0cb397ca3c6c2e23/src/analysis/20230814_exports/scRNA_data.ipynb)]
- `20230814_exports/snMultiome_ATAC_data.ipynb`and `20230814_exports/snMultiome_RNA_data.ipynb`: Same as above for snMultiome. For ATAC, used integration with D2 and provided transferred cluster labels. No labels provided for RNA. Note that order of cells is different between ATAC and RNA [[commit](https://github.com/kundajelab/scATAC-reprog/tree/f3fcca48824539cabd655d21917147a8806fde6b/src/analysis/20230814_exports)]
- `20230814_exports/prep_vitessce.ipynb`: prepared scRNA object for Vitessce browser GitHub pages deployment. Added endogenous and sendai OSKM expression to matrix. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/master/src/analysis/20230814_exports/prep_vitessce.ipynb)] [[reprogramming-vitessce](https://github.com/kundajelab/reprogramming-browser/tree/ff08ea0741d2be8bbc67ce5f98c36cc71e28abfa)]
- `20230814_exports/GO_sheet.ipynb`: Exported GO terms for peak set → gene sets along with the gene sets as an Excel sheet [[commit](https://github.com/kundajelab/scATAC-reprog/blob/1e73bcd0ec064baf00abb9549da33f60c8e70368/src/analysis/20230814_exports/GO_sheet.ipynb)] [[sheet](https://github.com/kundajelab/scATAC-reprog/blob/1e73bcd0ec064baf00abb9549da33f60c8e70368/src/analysis/20230814_exports/out/GO_terms.xlsx)]
- `20230814_exports/scATAC_cluster_data.ipynb` and `20230814_exports/models_data.ipynb`: Exported fragment files and peaks called per cluster, and for models: training bigwigs, peak + non peaks, outputs: shap + modisco. [[commit](https://github.com/kundajelab/scATAC-reprog/tree/1e73bcd0ec064baf00abb9549da33f60c8e70368/src/analysis/20230814_exports)]
- `20230814_exports/motifs.ipynb`: Exported consolidated motifs, their representative PFMs, and motif assignments for counts motifs of each cluster. [[commit](https://github.com/kundajelab/scATAC-reprog/blob/eecd8ca9fb142d6c51adea5af339c85f2b57add6/src/analysis/20230814_exports/motifs.ipynb)]
