from sys import argv

_, bedfile = argv

# TODO: write properly with tests
# does a greedy merge- if overlapping intervals, takes the one that ends first and discards the other

# bedfile should be sorted
f = open(bedfile)

first = f.readline().strip().split('\t')
cur_chrm = first[0]
cur_end = int(first[2])

print('\t'.join(first))

for line in f:
    cur_line = line.strip().split('\t')
    
    chrm, start, end = cur_line[0], int(cur_line[1]), int(cur_line[2])
    
    # if chrm change
    if chrm!=cur_chrm:
        cur_chrm = chrm
        cur_end = end
        print('\t'.join(cur_line))

    else:
        # BED is 0 indexed (right?)
        if start >= cur_end:
            cur_end = end
            print('\t'.join(cur_line))

f.close()
