#!/usr/bin/bash
#SBATCH --job-name=hist_4
#SBATCH --output=hist_4.out
#SBATCH --error=hist_4.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --array=2-20:2
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=ALL

python3 entropy_hist.py -n 2048 -T 256 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 100 -D 4