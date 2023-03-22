#!/bin/bash

#SBATCH --job-name=btmh5
#SBATCH --output=/home/users/surag/CS273B/model_zoo/stage1/log.txt
#SBATCH --error=/home/users/surag/CS273B/model_zoo/stage1/err.txt
#SBATCH --time=48:00:00

#SBATCH --partition=akundaje,owners

#SBATCH --nodes=1

#SBATCH --mem=52G

#SBATCH --gres=gpu:1

#SBATCH --cores-per-socket=8

#SBATCH --constraint="GPU_GEN:PSC|GPU_SKU:P100_PCIE|GPU_SKU:P40|GPU_SKU:RTX_2080Ti|GPU_SKU:V100_PCIE|GPU_SKU:V100S_PCIE|GPU_SKU:V100_SXM2"

# don't want to use A100
module load cuda/10.0
module load cudnn/7.4

# https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
eval "$(conda shell.bash hook)"
conda activate mtbatchgen

echo "Live"
python "$@"
