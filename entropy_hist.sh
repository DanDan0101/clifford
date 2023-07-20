#!/usr/bin/bash
#SBATCH --job-name=entropy_hist
#SBATCH --output=hist.out
#SBATCH --error=hist.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --ntasks=10
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.02 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.04 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.06 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.08 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.10 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.12 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.14 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.16 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.18 -s 1000 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_hist.py -n 512 -T 256 -p 0.20 -s 1000 &
wait