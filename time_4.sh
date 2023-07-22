#!/usr/bin/bash
#SBATCH --job-name=time_4
#SBATCH --output=time_4.out
#SBATCH --error=time_4.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --array=0-10,15,20
#SBATCH --ntasks=13
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4G
#SBATCH --mail-type=ALL

python3 time.py -n 2048 -T 300 -p $(printf 0.%02i $SLURM_ARRAY_TASK_ID) -s 10 -D 4