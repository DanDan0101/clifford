#!/usr/bin/bash
#SBATCH --job-name=info_512
#SBATCH --output=info_512.out
#SBATCH --error=info_512.err
#SBATCH --time=23:30:00
#SBATCH -p normal
#SBATCH --array=155-165
#SBATCH -c 16
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 info.py -L 512 -T 256 -p $(printf 0.%03i $SLURM_ARRAY_TASK_ID) -s 100 -t 100 -D 1