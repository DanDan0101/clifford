#!/usr/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job.%j.out
#SBATCH --error=test_job.%j.err
#SBATCH --time=00:30:00
#SBATCH -p normal
#SBATCH -c 1
#SBATCH --mem=8GB

python test.py