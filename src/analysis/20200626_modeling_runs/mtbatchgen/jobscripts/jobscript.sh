#!/bin/bash

#SBATCH --job-name=btmh5
#SBATCH --output=/home/users/surag/CS273B/model_zoo/stage1/log.txt
#SBATCH --error=/home/users/surag/CS273B/model_zoo/stage1/err.txt
#SBATCH --time=84:00:00

#SBATCH --partition=akundaje

#SBATCH --nodes=1

#SBATCH --mem=52G

#SBATCH --gres=gpu:1

#SBATCH --cores-per-socket=8

module load cudnn

# https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
eval "$(conda shell.bash hook)"
conda activate mtbatchgen

echo "Live"
python "$@"
