#!/bin/bash

#SBATCH --time=84:00:00
#SBATCH --partition=akundaje
#SBATCH --nodes=1

#SBATCH --mem=32G

#SBATCH --sockets-per-node=2
#SBATCH --cores-per-socket=8


# https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
eval "$(conda shell.bash hook)"
conda activate mtbatchgen

echo "Live"
"$@"
