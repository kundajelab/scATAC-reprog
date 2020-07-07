#!/bin/bash

#SBATCH --time=84:00:00
#SBATCH --partition=akundaje
#SBATCH --nodes=1

#SBATCH --mem=32G

#SBATCH --sockets-per-node=2
#SBATCH --cores-per-socket=8

echo "Live"
"$@"
