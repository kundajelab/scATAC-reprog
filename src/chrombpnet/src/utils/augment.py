import numpy as np

# https://stackoverflow.com/questions/46091111/python-slice-array-at-different-position-on-every-row
def take_per_row(A, indx, num_elem):
    """
    Matrix A, indx is a vector for each row which specifies 
    slice beginning for that row. Each has width num_elem.
    """
    all_indx = indx[:,None] + np.arange(num_elem)
    return A[np.arange(all_indx.shape[0])[:,None], all_indx]


def random_crop(seqs, labels, crop_width):
    """
    Takes sequences and corresponding counts labels. They should have the same
    #examples and width. Each example is cropped starting at a random offset.
    """
    assert(seqs.shape[1]>=crop_width)

    max_start = seqs.shape[1] - crop_width

    starts = np.random.choice(range(max_start+1), size=seqs.shape[0], replace=True)

    return take_per_row(seqs, starts, crop_width), take_per_row(labels, starts, crop_width)

def random_rev_comp(seqs, labels, frac=0.5):
    """
    Data augmentation: applies reverse complement randomly to a fraction of 
    sequences and labels.

    Assumes seqs are arranged in ACGT. Then ::-1 gives TGCA which is revcomp.

    NOTE: Performs in-place modification.
    """
    
    pos_to_rc = np.random.choice(range(seqs.shape[0]), 
            size=int(seqs.shape[0]*frac),
            replace=False)

    seqs[pos_to_rc] = seqs[pos_to_rc, ::-1, ::-1]
    labels[pos_to_rc] = labels[pos_to_rc, ::-1]

    return seqs, labels

def crop_revcomp_augment(seqs, labels, crop_width, rc_frac=0.5, shuffle=False):
    """
    seqs: B x L x 4
    labels: B x L

    Applies random crop to seqs and labels and reverse complements rc_frac.
    """
    assert(seqs.shape[0]==labels.shape[0])
    assert(seqs.shape[1]==labels.shape[1])

    # this does not modify seqs and labels
    mod_seqs, mod_labels = random_crop(seqs, labels, crop_width)
    
    # this modifies mod_seqs, mod_labels in-place
    mod_seqs, mod_labels = random_rev_comp(mod_seqs, mod_labels, frac=rc_frac)

    if shuffle:
        perm = np.random.permutation(mod_seqs.shape[0])
        mod_seqs = mod_seqs[perm]
        mod_labels = mod_labels[perm]

    return mod_seqs, mod_labels
