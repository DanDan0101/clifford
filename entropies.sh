#!/usr/bin/bash
#SBATCH --job-name=entropies
#SBATCH --output=entropies.out
#SBATCH --error=entropies.err
#SBATCH --time=6:00:00
#SBATCH -p hns
#SBATCH --array=1-24
#SBATCH -c 16
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 -u S_all.py -t $SLURM_ARRAY_TASK_ID
