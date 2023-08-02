#!/usr/bin/bash
#SBATCH --job-name=info_64
#SBATCH --output=info_64.out
#SBATCH --error=info_64.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=155-165
#SBATCH -c 8
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

python3 info.py -L 64 -T 32 -p $(printf 0.%03i $SLURM_ARRAY_TASK_ID) -s 10000 -t 100 -D 1