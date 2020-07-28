import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--motifs-subset-list", type=str, required=True)
parser.add_argument("-m", "--all-motifs", type=str, required=True)
parser.add_argument("-o", "--out-motif-file", type=str, required=True)

args = parser.parse_args()

# assumes each MOTIF beginning has the word "MOTIF" in it
with open(args.all_motifs) as f:
    all_motifs = f.readlines()

with open(args.motifs_subset_list) as f:
    selected_motifs = [x.strip() for x in f.readlines()]

with open(args.out_motif_file, 'w') as f:
    # start writing headers
    write_line = True

    for all_motifs_line in all_motifs:
        if "MOTIF" in all_motifs_line:
            write_line = any([y in all_motifs_line for y in selected_motifs]) # matches motif

        if write_line:
            f.write(all_motifs_line)
