#!/usr/bin/bash
#SBATCH --job-name=info_128
#SBATCH --output=info_128.out
#SBATCH --error=info_128.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=155-165
#SBATCH --ntasks=11
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

python3 info.py -L 128 -T 64 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 10000 -t 100 -D 1