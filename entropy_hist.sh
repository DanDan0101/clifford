#!/usr/bin/bash
#SBATCH --job-name=entropy_hist
#SBATCH --output=time.%j.out
#SBATCH --error=time.%j.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=ALL

python3 entropy_hist.py -n 512 -T 256 -s 1000