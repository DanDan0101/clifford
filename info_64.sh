#!/usr/bin/bash
#SBATCH --job-name=info_64
#SBATCH --output=info_64.out
#SBATCH --error=info_64.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=0-25,30,40,50
#SBATCH --ntasks=29
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

python3 info.py -L 64 -T 32 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 10000 -D 1