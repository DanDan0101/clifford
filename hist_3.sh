#!/usr/bin/bash
#SBATCH --job-name=hist_3
#SBATCH --output=hist_3.out
#SBATCH --error=hist_3.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --array=2-20:2
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=6G
#SBATCH --mail-type=ALL

python3 hist.py -n 1536 -T 256 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 100 -D 3