MoDISco runs derived from SVM on 50k seqlets. Scripts etc in `20200626_modeling_runs`. Copied over modisco outputs.

`for i in {1..18} ; do (mkdir cluster_idx$i/pfms ; python ~/kundajelab/surag-scripts/modisco/modisco_to_pfm.py -m cluster_idx$i/*.hdf5 -o cluster_idx$i/pfms) & done`

`for i in {1..18} ; do python ../../../scripts/fetch_tomtom.py -m cluster_idx$i/modisco_results.hdf5  -o cluster_idx$i/tomtom_matches.hocomoco.tsv -d ~/kundajelab/scATAC-reprog/resources/hocomoco/HOCOMOCOv11_core_HUMAN_mono_meme_format.meme & done`

`for i in {1..18} ; do python ../../../scripts/fetch_tomtom.py -m cluster_idx$i/modisco_results.hdf5  -o cluster_idx$i/tomtom_matches.homer.tsv -d ~/kundajelab/scATAC-reprog/resources/HOMER/homer_motifs.meme.txt & done`

For Vierstra Archetypes:
`for i in {1..18} ; do python ../../../../scripts/fetch_tomtom.py -m cluster_idx$i/modisco_results.hdf5  -o cluster_idx$i/tomtom_matches.vierstra.motif_archetypes.tsv -d /srv/www/kundaje/surag/resources/motif_archetypes/pfm_meme_format/motifs.meme.txt & done`
