#!/usr/bin/bash
#SBATCH --job-name=test_job
#SBATCH --output=test_job.%j.out
#SBATCH --error=test_job.%j.err
#SBATCH --time=12:00:00
#SBATCH -p hns
#SBATCH -c 1
#SBATCH --mem=8GB
#SBATCH --mail-type=ALL

python3 qiskit_test.py -n 512 -T 150 -p 0.06 -s 100