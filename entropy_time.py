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
args = parser.parse_args()

n_qubits = args.n_qubits
depth = args.T
shots = args.shots

ps = np.array([0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.15, 0.20])

entropies_zero = {}
entropies_me = {}

for p in ps:
    print("Evolving entropies for p = {}:".format(p))

    state = pc.zero_state(n_qubits)
    entropies_zero[p] = evolve_entropies(state, depth, p, shots)

    state = me_state(n_qubits)
    entropies_me[p] = evolve_entropies(state, depth, p, shots)

with open('{}_{}_{}_hist_zero.pkl'.format(n_qubits, depth, shots), 'wb') as f:
    pickle.dump(entropies_zero, f)

with open('{}_{}_{}_hist_me.pkl'.format(n_qubits, depth, shots), 'wb') as f:
    pickle.dump(entropies_me, f)