from copy import deepcopy
import json
import os

TEMPLATE = {
  "atac.pipeline_type": "atac",
  "atac.genome_tsv": "gs://encode-pipeline-genome-data/hg38_gcp.tsv",
  "atac.paired_end": True,
  "atac.enable_idr": True,
  "atac.idr_thresh": 0.05,
  "atac.xcor_cpu": 16,
  "atac.call_peak_mem_mb":50000,
  "atac.macs2_signal_track_mem_mb": 50000,
  "atac.align_disks": "local-disk 600 HDD"
}

JSONS_DIR = "/users/surag/kundajelab/scATAC-reprog/src/analysis/20200122_snapATAC/snapATAC_sessions/20200125_n76770/jsons/"
DATA_PREFIX = "gs://caper_in/scATAC-reprog/cluster_tagAlign"
NUM_CLUSTERS = 18

for i in range(1, NUM_CLUSTERS+1):
    cur_json = deepcopy(TEMPLATE)
    cur_json["atac.tas"] = ["{}/cluster_idx{}.tagAlign.gz".format(DATA_PREFIX, i)]
   
    f = open(os.path.join(JSONS_DIR, "cluster_idx{}.json".format(i)), 'w')
    json.dump(cur_json, f, indent=2)
    f.close()
