#!/usr/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job.%j.out
#SBATCH --error=test_job.%j.err
#SBATCH --time=12:00:00
#SBATCH -p normal
#SBATCH -c 1
#SBATCH --mem=4GB
#SBATCH --mail-type=ALL

python3 -u test.py -n 512 -T 150 -p 0.16 -s 100
