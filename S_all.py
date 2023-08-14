import sys
sys.path.insert(0, 'clifford')

import numpy as np
import pyclifford as pc
from MIPT import create_circuit, qubit_pos, xi, entropy
import time
import os
from multiprocess import Pool
num_cpus = len(os.sched_getaffinity(0))
print("Using {} CPUs.".format(num_cpus))

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves entropy graph to the current directory.'
)
parser.add_argument('-t', type = int, default = 1)
args = parser.parse_args()
t = args.t

# Parameter space [24]
# D: {2-5} [4]
# L: 2**{4-9} [6]
# p: pc
# depth: L/2
# timesteps: 128

t -= 1
# t is 0 to 23

D = 2 + int(t / 6)
t = t % 6

# t is 0 to 5
L = 2**(4 + t)

depth = int(L / 2)
shots = 256
timesteps = 128
N = L * D

p_dict = {
    1: 0.16,
    2: 0.33,
    3: 0.418,
    4: 0.458,
    5: 0.478
}
p = p_dict[D]

YT = 0.61

stub = "data/{}_{}_{}_{}_{}_".format(L, depth, shots * timesteps, p, D)

start_time = time.time()

print("Sampling all entropies for L = {}, D = {}, p = {}:".format(L, D, p))

def sample_all_entropies(state):
    result = []
    qubits = []
    for i in range(1, int(L / 2) + 1):
        qubits.extend(qubit_pos(i, D))
        x = xi(L, 0, i)
        y = entropy(state, D, qubits)
        result.append((x, y))
    return np.array(result)

def sample(dummy):
    circ = create_circuit(L, depth, p, D)
    state = pc.zero_state(N)
    circ.forward(state)
    buffer = sample_all_entropies(state)
    for i in range(timesteps - 1):
        circ = create_circuit(L, 1, p, D)
        circ.forward(state)
        buffer = np.vstack((buffer, sample_all_entropies(state)))
    return buffer

runs = np.repeat(0, shots)

with Pool(num_cpus) as pool:
    results = pool.map(sample, range(shots))

results = np.array(results).reshape((-1,int(L / 2),2))

means = np.mean(results, axis = 0)
stds = np.std(results[:, :, 1], axis = 0, ddof = 1) / np.sqrt(results.shape[0])

result = np.stack((means[:, 0], means[:, 1], stds))

end_time = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))
print("L = {}, D = {}, p = {} done in {}".format(L, D, p, end_time))

with open(stub + "entropies_all.npy", 'wb') as f:
    np.save(f, result)