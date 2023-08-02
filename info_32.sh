#!/usr/bin/bash
#SBATCH --job-name=info_32
#SBATCH --output=info_32.out
#SBATCH --error=info_32.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=155-165
#SBATCH -c 8
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

python3 info.py -L 32 -T 16 -p $(printf 0.%03i $SLURM_ARRAY_TASK_ID) -s 10000 -t 100 -D 1
