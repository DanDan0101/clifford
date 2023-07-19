import numpy as np
from tqdm import tqdm
import pyclifford as pc
from MIPT import create_circuit, entropy
import pickle

# Parse command line arguments
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

entropies = {}

ps = np.array([0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
for i, p in enumerate(ps):
    print("Evolving entropies for p = {}:".format(p))
    S_p = []
    for _ in tqdm(range(shots)):
        circ = create_circuit(n_qubits, depth, p)
        state = pc.zero_state(n_qubits)
        state = circ.forward(state)
        S_p.append(entropy(state))
    entropies[p] = np.array(S_p)

with open('{}_{}_{}_hist.pkl'.format(n_qubits, depth, shots), 'wb') as f:
    pickle.dump(entropies, f)