#!/usr/bin/bash
#SBATCH --job-name=entropies
#SBATCH --time=18:00:00
#SBATCH -p hns
#SBATCH --array=12,18,24,30
#SBATCH -c 16
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 -u S_all.py -t $SLURM_ARRAY_TASK_ID
