Added on 22 October 2020:

From Pmat.ipynb:
- features.50d.tsv: x.sp@smat@dmat (reduced dimension representation from diffusion maps for each barcode)  
- features.8d.tsv: same as above, for first 8 dimensions which are used for UMAP.
- metadata.tsv: contains UMAP coordinates + clusters (derived from 1st iteration in `20200122_snapATAC/snapATAC_sessions/20201020_n62402/`, but with cells in clusters 15 (clump) and 16 (iPSC) removed)
- peaks.bed: contains all peaks from snap files (not just those used for diff map + UMAP). No iPSC peaks or clump peaks (cluster 15).
- pmat.sparse.mm: contains raw insertions in each of the above peaks for each of the cells. No iPSC peaks or clump peaks.

Peak set used is merged overlap peaks after extending all summits 250 bp in either direction.
