library(GenomicRanges)
library(rtracklayer)
library(Matrix)

motif_hits_imp_thresh = read.table("motifs.importance.thresholded.bed", sep='\t')
colnames(motif_hits_imp_thresh) = c('chr', 'start', 'end', 'name', 'score', 'strand', 'seq')
motif_hits_imp_thresh = GRanges(motif_hits_imp_thresh)

all_peaks = import("../../../20200206_pmat_snapATAC/sessions/20210717_n62599/peaks.bed")

tfs = as.vector(read.table("./tfs_final.txt")$V1)

overlaps = findOverlaps(motif_hits_imp_thresh, all_peaks, type='within')

query_motif = motif_hits_imp_thresh[queryHits(overlaps)]$name

stopifnot(length(unique(query_motif))==length(tfs))
query_motif = factor(query_motif, levels=tfs)

all_peaks_x_motif = sparseMatrix(i=subjectHits(overlaps),
                                 j=as.numeric(query_motif),
                                 dims=c(length(all_peaks), length(levels(query_motif))),
                                dimnames=list(as.character(all_peaks), levels(query_motif)))

all_peaks_x_motif = as(all_peaks_x_motif, "dgCMatrix")

writeMM(all_peaks_x_motif,
        file="./peaks_x_importance_thresholded.mm")


