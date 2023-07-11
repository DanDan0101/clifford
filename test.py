from clifford import make, draw, run
from clifford import B, clipped_gauge, entropy
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves entropies to the current directory.'
)
parser.add_argument('-n', '--n_qubits', type = int, default = 512)
parser.add_argument('-T', type = int, default = 150)
parser.add_argument('-p', type = float, default = 0.06)
parser.add_argument('-s', '--shots', type = int, default = 1)
args = parser.parse_args()

n_qubits = args.n_qubits
T = args.T
p = args.p
shots = args.shots

stabs = []
print("Generating and simulating circuits:")
for _ in tqdm(range(shots)):
    circ = make(n_qubits, T, p, save_intermediate = False)
    # draw(circ)
    result = run(circ)
    stabs.append(result.data()['t'+str(2*T-1)][0]) # Append the final state

print("Calculating entropies:")
S = [entropy(stab_state, n_qubits // 2, n_qubits) for stab_state in tqdm(stabs)]
np.savetxt("S_{}_{}_{}_{}.out".format(n_qubits, T, p, shots), S)

plt.hist(S)
plt.show()