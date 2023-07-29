#!/usr/bin/bash
#SBATCH --job-name=info_32
#SBATCH --output=info_32.out
#SBATCH --error=info_32.err
#SBATCH --time=23:30:00
#SBATCH -p hns
#SBATCH --array=0-25,30,40,50
#SBATCH --ntasks=29
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

python3 info.py -L 32 -T 16 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 1000000 -D 1
