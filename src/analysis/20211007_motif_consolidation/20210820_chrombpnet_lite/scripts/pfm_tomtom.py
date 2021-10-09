import numpy as np
import os
import subprocess 
import argparse
import tempfile

def write_meme_file(ppm, bg, fname):
    f = open(fname, 'w')
    f.write('MEME version 4\n\n')
    f.write('ALPHABET= ACGT\n\n')
    f.write('strands: + -\n\n')
    f.write('Background letter frequencies (from unknown source):\n')
    f.write('A %.3f C %.3f G %.3f T %.3f\n\n' % tuple(list(bg)))
    f.write('MOTIF 1 TEMP\n\n')
    f.write('letter-probability matrix: alength= 4 w= %d nsites= 1 E= 0e+0\n' % ppm.shape[0])
    for s in ppm:
        f.write('%.5f %.5f %.5f %.5f\n' % tuple(s))
    f.close()


def fetch_tomtom_matches(ppm, background=[0.25, 0.25, 0.25, 0.25], tomtom_exec_path='tomtom', motifs_db='HOCOMOCOv11_core_HUMAN_mono_meme_format.meme' , 
        n=5):
    """Fetches top matches from a motifs database using TomTom.
    
    Args:
        ppm: position probability matrix- numpy matrix of dimension (N,4)
        background: list with ACGT background probabilities
        tomtom_exec_path: path to TomTom executable
        motifs_db: path to motifs database in meme format
        n: number of top matches to return, ordered by p-value
   
    
    Returns:
        list: a list of up to n results returned by tomtom, each entry is a
            dictionary with keys 'Target ID', 'p-value', 'E-value', 'q-value'  
    """
    
    _, fname = tempfile.mkstemp()
    
     
    # trim and prepare meme file
    write_meme_file(ppm, background, fname)
    
    # run tomtom
    cmd = '%s -no-ssc -oc . -verbosity 1 -text -min-overlap 5 -mi 1 -dist pearson -evalue -thresh 10.0 %s %s' % (tomtom_exec_path, fname, motifs_db)
    #print(cmd)
    out = subprocess.check_output(cmd, shell=True)
    print(out.decode('utf-8'))

def fetch_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pfm", required=True, type=str, help="one motif per file, pre-trimmed, tab separated, no header/annotation")
    parser.add_argument("-d", "--meme_motif_db", required=True, type=str)
    parser.add_argument("-n", "--top_n_matches", type=int, default=3, help="Max number of matches to return from TomTom")
    parser.add_argument("-tt", "--tomtom_exec", type=str, default='tomtom')
    args = parser.parse_args()
    return args

if __name__=="__main__":
    args = fetch_args()
    
    ppm = []
    with open(args.pfm) as f:
        for x in f:
            ppm.append([float(y) for y in x.strip().split('\t')])
    # normalize
    ppm = [[y/sum(x) for y in x] for x in ppm]

    fetch_tomtom_matches(np.array(ppm), tomtom_exec_path=args.tomtom_exec, motifs_db=args.meme_motif_db, 
            n=args.top_n_matches) 

