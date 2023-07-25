#!/usr/bin/bash
for i in {2..5}
do
    sbatch hist_${i}.sh
    sbatch time_zero_${i}.sh
    sbatch time_me_${i}.sh
done