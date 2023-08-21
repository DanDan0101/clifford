import sys
sys.path.insert(0, 'clifford')

import numpy as np
from MIPT import xi, entropy, sample
import time
import os
from multiprocess import Pool
num_cpus = len(os.sched_getaffinity(0))
print("Using {} CPUs.".format(num_cpus))

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves entropies to the current directory.'
)
parser.add_argument('-t', type = int, default = 1)
args = parser.parse_args()
t = args.t

# Parameter space [30]
# D: {1-5} [5]
# L: 2**{4-9} [6]
# p: pc
# depth: L // 2
# timesteps: 256

t -= 1
# t is 0 to 29

D = 1 + t // 6
t = t % 6

# t is 0 to 5
L = 2**(4 + t)

depth = L // 2
shots = 16
timesteps = 256
TIMELIMIT = 60 * 60 * 10 # 10 hours
MAXRUNS = 64

N = L * D

p_dict = {
    1: 0.15967,
    2: 0.32865,
    3: 0.416,
    4: 0.458,
    5: 0.4792
}
p = p_dict[D]

start_time = time.time()

print("Sampling all entropies for L = {}, D = {}, p = {}:".format(L, D, p))

def f(state):
    result = []
    qudits = [0]
    for i in range(1, L // 2 + 1):
        qudits.append(i)
        result.append(entropy(state, D, qudits))
    return np.array(result)

run = 0
accumulator = np.zeros((2, L // 2))

start_time = time.time()

while time.time() - start_time < TIMELIMIT and run < MAXRUNS:
    with Pool(num_cpus) as pool:
        results = pool.starmap(lambda: sample(f, L, p, D, timesteps, depth), [[]] * shots)
    results = np.mean(np.array(results), axis = 0)
    accumulator += results
    run += 1

    mean = accumulator[0, :] / run
    std = np.sqrt(accumulator[1, :] / run - mean**2) / np.sqrt(run * shots * timesteps)
    result = np.stack((mean, std))
    stub = "data/{}_{}_{}_{}_{}_".format(L, depth, run * shots * timesteps, p, D)
    with open(stub + "entropies_all.npy", 'wb') as filename:
        np.save(filename, result)

end_time = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))
print("L = {}, D = {}, p = {} done in {}, completed {} runs.".format(L, D, p, end_time, run))