import sys
sys.path.insert(0, 'clifford')

import numpy as np
from MIPT import evolve_entropies
import time

# Parse command line arguments
import argparse
parser = argparse.ArgumentParser(
    description = 'Run the Clifford circuit simulation.',
    epilog = 'Saves time-evolution of entropies to the current directory.'
)
parser.add_argument('-L', type = int, default = 512)
parser.add_argument('-T', type = int, default = 256)
parser.add_argument('-s', '--shots', type = int, default = 10)
parser.add_argument('-p', type = float, default = 0.1)
parser.add_argument('-D', type = int, default = 1)
args = parser.parse_args()

L = args.L
depth = args.T
shots = args.shots
p = args.p
D = args.D
N = L * D
stub = "data/{}_{}_{}_{}_{}_".format(L, depth, shots, p, D)

ctime = time.time()

print("Evolving entropies for p = {}:".format(p))

entropies_zero = evolve_entropies(L, depth, p, True, shots, D = D, logging = False)

wtime = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - ctime)))
print("p = {} done in {}".format(p, wtime))

with open(stub + "zero.npy", 'wb') as f:
    np.save(f, entropies_zero)