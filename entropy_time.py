import sys
sys.path.insert(0, 'clifford')

import numpy as np
import pyclifford as pc
from MIPT import evolve_entropies, me_state
import time

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves time-evolution of entropies to the current directory.'
)
parser.add_argument('-n', '--n_qubits', type = int, default = 512)
parser.add_argument('-T', type = int, default = 256)
parser.add_argument('-s', '--shots', type = int, default = 10)
parser.add_argument('-p', type = float, default = 0.1)
args = parser.parse_args()

n_qubits = args.n_qubits
depth = args.T
shots = args.shots
p = args.p
stub = "{}_{}_{}_{}_".format(n_qubits, depth, shots, p)

ctime = time.time()

print("Evolving entropies for p = {}:".format(p))

state = pc.zero_state(n_qubits)
entropies_zero = evolve_entropies(state, depth, p, shots, logging = False)

wtime = time.time() - ctime
print("p = {} zero state done in {}:{}:{}".format(p, wtime//3600, (wtime//60)%60, wtime%60))

with open(stub + "zero.npy", 'wb') as f:
    np.save(f, entropies_zero)

state = me_state(n_qubits)
entropies_me = evolve_entropies(state, depth, p, shots, logging = False)

wtime = time.time() - ctime
print("p = {} done in {}:{}:{}".format(p, wtime//3600, (wtime//60)%60, wtime%60))

with open(stub + "me.npy", 'wb') as f:
    np.save(f, entropies_me)