"""
Takes a directory of fastqs where R1,R3 are reads and R2 are barcodes. Takes a text file
with one read name (e.g. J00118:471:H773LBBXY:1:1101:10003:10106) per line. For each name, 
outputs the barcode in the same order. Prints output to stdout.

Useful when demuxing was not done initially.

Automatically selects fastqs from directory that have "R2" in them and end with ".bam".
"""

import argparse
import gzip
import os
import tqdm
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--read_name_file", help="Input read name file", type=str, required=True)
parser.add_argument("-f", "--fastq_dir", help="Path to fastq dir", type=str, required=True)
parser.add_argument("-o", "--output", help="Output filename (gzipped)", type=str, required=True)
args = parser.parse_args()

if __name__=="__main__":
    # get list of fastqs R1 and R2
    index_fastqs = [os.path.join(args.fastq_dir,x) for x in os.listdir(args.fastq_dir) if x.endswith(".fastq.gz") and "R2" in x]
    
    print("INDEX FASTQS : ")
    for x in index_fastqs:
        print("-- " + x)

    # open bam
    with gzip.open(args.read_name_file) as rnf: 
        # get names from bam, adding @ explicitly
        read_names = ["@" + x.decode('utf-8').strip() for x in rnf]
     
    names_set = set(read_names)
    print("GOT BAM: {} names".format(len(names_set)))

    name_to_barcode_dict = {}

    # not checking for name duplication
    cur_name = ''
    with tqdm.tqdm(total=len(names_set)) as pbar:
       for ifq in index_fastqs:
           with gzip.open(ifq) as f1:
               for i,l1 in enumerate(f1):
                   if i%4==0:
                       cur_name = l1.decode('utf-8').strip().split(' ')[0]
                   elif i%4==1:
                       if cur_name in names_set:
                           name_to_barcode_dict[cur_name] = l1.decode('utf-8').strip()
                           names_set.remove(cur_name)
                           pbar.update(1)

                           if len(names_set)==0:
                               break
           if len(names_set)==0:
               break
    
    print("GOT BARCODES, WRITING OUTPUT")
    with gzip.open(args.output, 'w') as f:
        for x in read_names:
            s = name_to_barcode_dict[x] + "\n"
            f.write(s.encode())
