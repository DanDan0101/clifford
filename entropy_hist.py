import sys
sys.path.insert(0, 'clifford')

import numpy as np
import pyclifford as pc
from MIPT import create_circuit, entropy
import time

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves final entropies to the current directory.'
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
S_p = []
for _ in range(shots):
    circ = create_circuit(n_qubits, depth, p)
    state = pc.zero_state(n_qubits)
    state = circ.forward(state)
    S_p.append(entropy(state))
S_p = np.array(S_p)

wtime = time.time() - ctime
print("p = {} done in {}:{}:{}".format(p, wtime//3600, (wtime//60)%60, wtime%60))

with open(stub + "hist.npy", 'wb') as f:
    np.save(f, S_p)