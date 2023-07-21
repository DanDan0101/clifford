#!/usr/bin/bash
#SBATCH --job-name=entropy_time
#SBATCH --output=time.out
#SBATCH --error=time.err
#SBATCH --time=24:00:00
#SBATCH -p hns
#SBATCH --ntasks=13
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1G
#SBATCH --mail-type=ALL

srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.01 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.02 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.03 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.04 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.05 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.06 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.07 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.08 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.09 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.10 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.15 -s 10 -D 2 &
srun --exclusive -n 1 -N 1 -c 1 python3 entropy_time.py -n 1024 -T 300 -p 0.20 -s 10 -D 2 &
wait