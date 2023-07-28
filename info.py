import sys
sys.path.insert(0, 'clifford')

import numpy as np
import pyclifford as pc
from MIPT import create_circuit, bip_info, trip_info
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

MAX_TIME = 60 * 60 * 23 # 23 hours
start_time = time.time()

print("Sampling information for p = {}:".format(p))

I_bip = []
I_trip = []
for i in range(shots):
    if time.time() - start_time > MAX_TIME:
        print("Exiting early at shot {}.".format(i))
        shots = i
        break
    circ = create_circuit(L, depth, p, D = D)
    state = pc.zero_state(N)
    circ.forward(state)
    I_bip.append(bip_info(state, D = D))
    I_trip.append(trip_info(state, D = D))

I_bip = np.array(I_bip)
bip_stats = np.array([np.mean(I_bip), np.std(I_bip, ddof = 1) / np.sqrt(shots)])
I_trip = np.array(I_trip)
trip_stats = np.array([np.mean(I_trip), np.std(I_trip, ddof = 1) / np.sqrt(shots)])
stats = np.stack((bip_stats, trip_stats))

end_time = time.strftime('%H:%M:%S', time.gmtime(int(time.time() - start_time)))
print("p = {} done in {}".format(p, end_time))

with open(stub + "info.npy", 'wb') as f:
    np.save(f, stats)