#!/usr/bin/bash
for i in {4..9}
do
    sbatch info_$((2**i)).sh
done