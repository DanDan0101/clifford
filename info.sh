#!/usr/bin/bash
#SBATCH --job-name=info
#SBATCH --time=12:00:00
#SBATCH -p hns
#SBATCH --array=1-330
#SBATCH -c 8
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 info.py -t $SLURM_ARRAY_TASK_ID
