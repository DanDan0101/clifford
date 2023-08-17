import sys
sys.path.insert(0, 'clifford')

import numpy as np
from MIPT import sample, trip_info
import time
import os
from multiprocess import Pool

num_cpus = len(os.sched_getaffinity(0))
print("Using {} CPUs.".format(num_cpus))

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves mean, std of tripartite information to the data directory.'
)
parser.add_argument('-t', type = int, default = 1)
args = parser.parse_args()
t = args.t

# Parameter space [330]
# D: {1-5} [5]
# L: 2**{4-9} [6]
# p: pc +/- 0.005 [11]
# depth: L // 2

t -= 1
# t is 0 to 329

D = 1 + t // 66
t %= 66

# t is 0 to 65
L = 2**(4 + t // 11)
t %= 11

p_dict = {
    1: 0.16,
    2: 0.33,
    3: 0.418,
    4: 0.458,
    5: 0.478
}

# t is 0 to 10
p = p_dict[D] + 0.001 * (t - 5)

depth = L // 2
shots = 32
timesteps = 256
TIMELIMIT = 60 * 60 * 11 # 11 hours
MAXRUNS = 32

N = L * D

start_time = time.time()

print("Sampling information for L = {}, D = {}, p = {}:".format(L, D, p))

f = lambda state: trip_info(state, D)

run = 0
accumulator = np.zeros(2)

while time.time() - start_time < TIMELIMIT and run < MAXRUNS:
    with Pool(num_cpus) as pool:
        results = pool.starmap(lambda: sample(f, L, p, D, timesteps, depth), [[]] * shots)
    results = np.mean(np.array(results), axis = 0)
    accumulator += results
    run += 1
accumulator /= run

mean = accumulator[0]
std = np.sqrt(accumulator[1] - mean**2) / np.sqrt(run * shots * timesteps)

result = np.array((mean, std))

stub = "data/{}_{}_{}_{}_{}_".format(L, depth, run * shots * timesteps, p, D)

with open(stub + "info.npy", 'wb') as f:
    np.save(f, result)

end_time = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))
print("L = {}, D = {}, p = {} done in {}, completed {} runs.".format(L, D, p, end_time, run))