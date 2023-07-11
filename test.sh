#!/usr/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job.%j.out
#SBATCH --error=test_job.%j.err
#SBATCH --time=01:00:00
#SBATCH -p normal
#SBATCH -c 4
#SBATCH --mem=16GB
#SBATCH --mail-type=ALL

python3 -u test.py -n 512 -T 150 -p 0.06 -s 4
