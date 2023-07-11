from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import Aer, transpile
from qiskit.quantum_info import random_clifford
import random

import numpy as np
import galois
GF = galois.GF(2)

def make(n_qubits, T, p, save_intermediate = False):
    """Generate a random Clifford QuantumCircuit.

    Args:
        n_qubits (int): number of qubits
        T (int): 2 * number of time steps
        p (float): probability of measurement
        save_intermediate (bool): whether to save the state after each time step
    
    Returns:
        A QuantumCircuit object.
    """
    qr = QuantumRegister(n_qubits, 'q')
    cr = ClassicalRegister(n_qubits, 'c')
    circ = QuantumCircuit(qr, cr)

    for t in range(T):
        # Layer 1
        for i in range(n_qubits // 2):
            circ.append(random_clifford(2), [qr[2*i], qr[2*i+1]])
        
        for i in range(n_qubits):
            if random.random() < p:
                circ.measure(qr[i], cr[i])
        
        if save_intermediate:
            circ.save_state(pershot = True, label = "t"+str(2*t))

        # Layer 2
        for j in range((n_qubits - 1) // 2):
            circ.append(random_clifford(2), [qr[2*j+1], qr[2*j+2]])
        
        # Periodic boundary conditions
        if n_qubits % 2 == 0:
            circ.append(random_clifford(2), [qr[-1], qr[0]])
        
        for j in range(n_qubits):
            if random.random() < p:
                circ.measure(qr[j], cr[j])

        if save_intermediate:
            circ.save_state(pershot = True, label = "t"+str(2*t+1))

    # Save final state
    if not save_intermediate:
        circ.save_state(pershot = True, label = "t"+str(2*T-1))
    return circ

def draw(circ):
    """Draw a Clifford QuantumCircuit.
    
    Args:
        circ (QuantumCircuit): a Clifford QuantumCircuit object
    """
    style = {
        'displaytext': {
            'clifford': r'\mathbf{C}_2'
        }
    }
    circ.draw('mpl', style = style, plot_barriers = False)

def run(circ, shots = 1):
    """Run a Clifford QuantumCircuit on the stabilizer simulator.
    
    Args:
        circ (QuantumCircuit): a Clifford QuantumCircuit object
        shots (int): number of shots
    
    Returns:
        A Result object containing a list of stabilizer states.
    """
    simulator = Aer.get_backend('aer_simulator_stabilizer')
    circ = transpile(circ, simulator)
    result = simulator.run(circ, shots = shots).result()
    return result

def B(G, n_qubits):
    """Compute bigrams of a stabilizer tableau.
    
    """
    rv = []
    for i in range(n_qubits): # loop through rows
        l = np.inf
        r = -np.inf
        for j in range(n_qubits): # loop through columns
            if G[i, 2*j] == 1 or G[i, 2*j+1] == 1:
                l = min(l, j)
                r = max(r, j)
        rv.append((l, r))
    return np.array(rv)

def clipped_gauge(stab_state, n_qubits):
    cliff = stab_state.clifford
    tableau = GF(cliff.stab.astype(int))[:, :-1]
    # Convert from X|Z to xz...xz, and convert to standard order
    stab = np.empty_like(tableau)
    stab[:, 0::2] = tableau[:, n_qubits-1::-1]
    stab[:, 1::2] = tableau[:, :n_qubits-1:-1]
    # Pregauge transformation
    stab = stab.row_reduce()
    # Gauge transformation (TODO)
    rev = stab[::-1, ::-1]
    rowset = set()
    for j in range(2 * n_qubits):
        col = rev[:, j]
        rows = np.nonzero(col)[0]
        if len(rows) == 0:
            continue
        if len(rows) == 1:
            rowset.add(rows[0])
            continue
        for i, row in enumerate(rows):
            if row not in rowset:
                rowset.add(row)
                if i != len(rows) - 1:
                    rev[rows[i+1:],:] += rev[row,:]
    return rev[::-1, ::-1]

def entropy(stab_state, A, n_qubits):
    cliff = stab_state.clifford
    tableau = GF(cliff.stab.astype(int))[:, :-1]
    # Convert from X|Z to xz...xz, and standard order of qubits
    stab = np.empty_like(tableau)
    stab[:, 0::2] = tableau[:, n_qubits-1::-1]
    stab[:, 1::2] = tableau[:, :n_qubits-1:-1]

    return np.linalg.matrix_rank(stab[:,:2*A]) - A