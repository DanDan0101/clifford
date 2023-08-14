#!/usr/bin/bash
#SBATCH --job-name=entropies
#SBATCH --output=entropies.out
#SBATCH --error=entropies.err
#SBATCH --time=9:00:00
#SBATCH -p hns
#SBATCH --array=1-24
#SBATCH -c 8
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 -u S_all.py -t $SLURM_ARRAY_TASK_ID