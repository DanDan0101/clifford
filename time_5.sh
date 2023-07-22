#!/usr/bin/bash
#SBATCH --job-name=time_5
#SBATCH --output=time_5.out
#SBATCH --error=time_5.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --array=0-10,15,20
#SBATCH --ntasks=13
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=5G
#SBATCH --mail-type=ALL

python3 time.py -n 2560 -T 300 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 10 -D 5