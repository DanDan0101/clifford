#!/usr/bin/bash
#SBATCH --job-name=info_256
#SBATCH --output=info_256.out
#SBATCH --error=info_256.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=155-165
#SBATCH --ntasks=11
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=2G
#SBATCH --mail-type=ALL

python3 info.py -L 256 -T 128 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 1000 -t 100 -D 1