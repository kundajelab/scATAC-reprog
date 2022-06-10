import argparse
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument("--all-bc", "-a", required=True, type=str)
parser.add_argument("--cell-bc", "-c", required=True, type=str)
parser.add_argument("--outfile", "-o", required=True, type=str)
args = parser.parse_args()


with open(args.all_bc) as f:
    all_bc = OrderedDict([(x.strip(),None) for x in f])

with open(args.cell_bc) as f:
    cell_bc = OrderedDict([(x.strip(),None) for x in f])

with open(args.outfile, 'w') as f:
    f.write("barcode,is__cell_barcode\n")
    for x in all_bc:
        f.write("{},{}\n".format(x, int(x in cell_bc)))
