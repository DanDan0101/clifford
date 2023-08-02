import sys
sys.path.insert(0, 'clifford')

import numpy as np
import pyclifford as pc
from MIPT import create_circuit, trip_info
import time
import os
from multiprocess import Pool
num_cpus = len(os.sched_getaffinity(0))
print("Using {} CPUs.".format(num_cpus))

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves time-evolution of information to the current directory.'
)
parser.add_argument('-L', type = int, default = 512)
parser.add_argument('-T', type = int, default = 256)
parser.add_argument('-s', '--shots', type = int, default = 10)
parser.add_argument('-t', type = int, default = 10)
parser.add_argument('-p', type = float, default = 0.1)
parser.add_argument('-D', type = int, default = 1)
args = parser.parse_args()

L = args.L
depth = args.T
shots = args.shots
timesteps = args.t
p = args.p
D = args.D
N = L * D
stub = "data/{}_{}_{}_{}_{}_".format(L, depth, shots * timesteps, p, D)

MAX_TIME = 60 * 60 * 23 # 23 hours
start_time = time.time()

print("Sampling information for p = {}:".format(p))

def sample_trip(p):
    """Samples tripartite information.

    Args:
        p (float): The probability of measuring a qudit.
    
    Returns:
        float: The average tripartite information.
        float: The tripartite information at the end of the circuit.
    """
    trips = []
    circ = create_circuit(L, depth, p, D = D)
    state = pc.zero_state(N)
    circ.forward(state)
    trips.append(trip_info(state, D = D))

    for _ in range(timesteps - 1):
        circ = create_circuit(L, 1, p, D = D)
        circ.forward(state)
        trips.append(trip_info(state, D = D))
    
    trips = np.array(trips)
    return np.mean(trips), trips[-1]

runs = np.repeat(p, shots)

with Pool(num_cpus) as pool:
    result = pool.map(sample_trip, runs)

result = np.array(result)
result = np.reshape(result, (-1, 2))
std = np.std(result[:, 1], ddof = 1)
result = np.mean(result, axis = 0)
result[1] = std / np.sqrt(runs.shape[0])

end_time = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))
print("p = {} done in {}".format(p, end_time))

with open(stub + "info.npy", 'wb') as f:
    np.save(f, result)