import argparse
import gzip
import os
from multiprocessing import Pool
import subprocess

"""
This script takes a metadata file with sample, barcode and cluster columns.
Goes through the tagAlign (with barcode in last column)for each cluster and
pushes out reads to appropriate clusters.
Ultimately makes one tagAlign for each cluster (without barcodes).
"""

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--metadata", type=str, required=True, help='TSV file which must have columns barcode, sample and cluster')
parser.add_argument("-st", "--sample_to_tagalign", type=str, required=True, help='each line: sample<tab>path/to/sample/tagalign')
parser.add_argument("-o", "--outdir", type=str, required=True)
parser.add_argument("-p", "--parallel", type=int, default=20)
args = parser.parse_args()

# read sample_to_tagAlign
f = open(args.sample_to_tagalign)
sample_to_tagalign = [x.strip().split('\t') for x in f]
f.close()
sample_to_tagalign = {x[0]:x[1] for x in sample_to_tagalign}

# prepare metadata
f = open(args.metadata)
metadata = [x.strip().split('\t') for x in f]
f.close()

metadata = {metadata[0][i]:[x[i] for x in metadata[1:]] for i in range(len(metadata[0]))}

sample_barcode_to_cluster = {x:dict() for x in set(metadata['sample'])}
for i in range(len(metadata['barcode'])):
    sample_barcode_to_cluster[metadata['sample'][i]][metadata['barcode'][i]] = metadata['cluster'][i]

assert(set(sample_to_tagalign.keys())==set(metadata['sample']))

#for sample in sample_barcode_to_cluster:
#    for bc in sample_barcode_to_cluster[sample]:
#        print(sample, bc, sample_barcode_to_cluster[sample][bc])

def sample_tagAlign_split(sample, barcode_to_cluster, tagAlign_path, outdir):
    clst_to_file = {}
    clst_to_barcode = {x:set() for x in set(barcode_to_cluster.values())} # return reads from which barcodes were added to each cluster

    # open out files
    for clst in set(barcode_to_cluster.values()):
        clst_to_file[clst] = gzip.open(os.path.join(outdir, "cluster_idx{}.sample_{}.tagAlign.gz".format(clst, sample)), 'w')
    
    f = gzip.open(tagAlign_path)
    
    #i = 0
    
    for x in f:
        s = x.decode('utf-8').strip().split('\t')
        # print(s[6])
        # 7th column should be barcode
        if s[6] in barcode_to_cluster: 
            # remove barcode before writing
            clst_to_file[barcode_to_cluster[s[6]]].write(('\t'.join(s[:6])+'\n').encode())
            clst_to_barcode[barcode_to_cluster[s[6]]].add('{}_{}'.format(sample, s[6]))
     #       i+=1
     #   if i==1000:
     #       break

    f.close()

    for x in clst_to_file:
        clst_to_file[x].close()

    return clst_to_barcode

p = Pool(args.parallel)
clst_to_barcodes_found = p.starmap(sample_tagAlign_split, [(sample, sample_barcode_to_cluster[sample], sample_to_tagalign[sample], args.outdir) for sample in sample_to_tagalign])

# merge cluster wise and delete rest
for clst in set(metadata['cluster']):
    f = open(os.path.join(args.outdir, "cluster_idx{}.tagAlign.gz".format(clst)), 'wb')
    subprocess.check_call(['cat {}/cluster_idx{}.sample_*'.format(args.outdir, clst)], shell=True, stdout=f)
    f.close()

    subprocess.check_call(['rm {}/cluster_idx{}.sample_*'.format(args.outdir, clst)], shell=True)

# Robustness check reports
cluster_to_sample_barcode = {x:set() for x in set(metadata['cluster'])}
for i in range(len(metadata['barcode'])):
    cluster_to_sample_barcode[metadata['cluster'][i]].add('{}_{}'.format(metadata['sample'][i], metadata['barcode'][i]))
cluster_barcodes_found_count = {x:0 for x in set(metadata['cluster'])}

# report which barcodes from which samples went to which cluster
f = open(os.path.join(args.outdir, "barcodes_added.tsv"), 'w')
f.write('sample\tbarcode\tcluster\n')
for x in clst_to_barcodes_found:
    for clst in x:
        for sample_barcode in x[clst]:
            assert(sample_barcode in cluster_to_sample_barcode[clst])
            sample, barcode = sample_barcode.split('_')
            cluster_barcodes_found_count[clst] += 1
            f.write('{}\t{}\t{}\n'.format(sample, barcode, clst))
f.close()

# for each cluster, report number of barcodes successfully found
f = open(os.path.join(args.outdir, "report.tsv"), 'w')
f.write("cluster\tbarcodes_found\tbarcodes_total\n")
for clst in cluster_barcodes_found_count:
    f.write("{}\t{}\t{}\n".format(clst, cluster_barcodes_found_count[clst], len(cluster_to_sample_barcode[clst])))
f.close()

