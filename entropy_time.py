import numpy as np
from tqdm import tqdm
import pyclifford as pc
from MIPT import evolve_entropies, me_state
import pickle

import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves entropies to the current directory.'
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

print("Evolving entropies for p = {}:".format(p))

state = pc.zero_state(n_qubits)
entropies_zero = evolve_entropies(state, depth, p, shots)

state = me_state(n_qubits)
entropies_me = evolve_entropies(state, depth, p, shots)

with open('{}_{}_{}_{}_zero.pkl'.format(n_qubits, depth, shots, p), 'wb') as f:
    pickle.dump(entropies_zero, f)

with open('{}_{}_{}_{}_me.pkl'.format(n_qubits, depth, shots, p), 'wb') as f:
    pickle.dump(entropies_me, f)