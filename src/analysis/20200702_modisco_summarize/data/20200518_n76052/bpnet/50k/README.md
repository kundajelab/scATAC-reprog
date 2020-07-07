MoDISco runs derived from SHAP scores on counts of 50k seqlets. Scripts etc in `???`. Copied over modisco outputs.

`for i in {1..18} ; do (mkdir cluster_idx$i/pfms ; python ~/kundajelab/surag-scripts/modisco/modisco_to_pfm.py -m cluster_idx$i/*.hdf5 -o cluster_idx$i/pfms) & done`

`for i in {1..18} ; do python ../../../scripts/fetch_tomtom.py -m cluster_idx$i/modisco_results.hdf5  -o cluster_idx$i/tomtom_matches.hocomoco.tsv -d ~/kundajelab/scATAC-reprog/resources/hocomoco/HOCOMOCOv11_core_HUMAN_mono_meme_format.meme & done`

`for i in {1..18} ; do python ../../../scripts/fetch_tomtom.py -m cluster_idx$i/modisco_results.hdf5  -o cluster_idx$i/tomtom_matches.homer.tsv -d ~/kundajelab/scATAC-reprog/resources/HOMER/homer_motifs.meme.txt & done`
