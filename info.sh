#!/usr/bin/bash
#SBATCH --job-name=info
#SBATCH --output=info.out
#SBATCH --error=info.err
#SBATCH --time=3:00:00
#SBATCH -p hns
#SBATCH --array=1-985
#SBATCH -c 8
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=ALL

python3 -u info.py -t $SLURM_ARRAY_TASK_ID