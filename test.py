from clifford import make, draw, run
from clifford import B, clipped_gauge, entropy
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

n_qubits = 512
T = 150
p = 0.06
shots = 1

circ = make(n_qubits, T, p, save_intermediate = False)
# draw(circ)
result = run(circ, shots = shots)

stabs = result.data()['t'+str(2*T-1)] # List of final states

S = [entropy(stab_state, 256) for stab_state in tqdm(stabs)]
np.savetxt("S_{}_{}_{}_{}.out".format(n_qubits, T, p, shots), S)

plt.hist(S)