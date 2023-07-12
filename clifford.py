from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, transpile
from qiskit.providers.aer import Aer
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
            circ.save_clifford(pershot = True, label = "t"+str(2*t))

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
            circ.save_clifford(pershot = True, label = "t"+str(2*t+1))

    # Save final state
    if not save_intermediate:
        circ.save_clifford(pershot = True, label = "t"+str(2*T-1))
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

def B(G):
    """Compute bigrams of a stabilizer tableau.

    Args:
        G (galois.FieldArray): a stabilizer tableau xz...xz of shape (n_qubits, 2 * n_qubits)
        n_qubits (int): number of qubits
    
    Returns:
        A numpy.ndarray of shape (n_qubits, 2) containing the bigrams.
    """
    n_qubits = G.shape[0]
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

def counts_B(bigrams):
    """Dev tool to count the number of occurrences of each endpoint.
    
    Args:
        bigrams (numpy.ndarray): a matrix of shape (n_qubits, 2) containing the bigrams.
    
    Returns:
        A numpy.ndarray of shape (n_qubits, 2) containing rho_l, rho_r, and rho.
    """
    n_qubits = bigrams.shape[0]
    rho_l = np.zeros(n_qubits, dtype = int)
    rho_r = np.zeros(n_qubits, dtype = int)
    for i in range(n_qubits):
        rho_l[i] = np.count_nonzero(bigrams[:, 0] == i)
        rho_r[i] = np.count_nonzero(bigrams[:, 1] == i)
    rho = rho_l + rho_r
    return np.stack((rho_l, rho_r, rho), axis = 1)

def entropy_B(bigrams, A):
    """Compute the entanglement entropy of a subsystem of a stabilizer state, given clipped-gauge bigrams.
    
    Args:
        bigrams (numpy.ndarray): a matrix of shape (n_qubits, 2) containing the bigrams in the clipped gauge.
        A (int): number of qubits in the subsystem of interest
    
    Returns:
        The entanglement entropy of the subsystem.
    """
    return np.count_nonzero(np.logical_and(bigrams[:, 0] < A, bigrams[:, 1] >= A)) / 2

def entropy(cliff, A):
    """Compute the entanglement entropy of a subsystem of a stabilizer state.

    Args:
        cliff (numpy.ndarray): a Clifford matrix X|Z of shape (n_qubits, 2 * n_qubits + 1)
        A (int): number of qubits in the subsystem of interest

    Returns:
        The entanglement entropy of the subsystem.
    """
    tableau = GF(cliff)[:, :-1] # Discard parity bit
    n_qubits = tableau.shape[0]
    # Convert from X|Z to xz...xz, and standard order of qubits
    stab = np.empty_like(tableau)
    stab[:, 0::2] = tableau[:, n_qubits-1::-1]
    stab[:, 1::2] = tableau[:, :n_qubits-1:-1]

    return np.linalg.matrix_rank(stab[:,:2*A]) - A

def clipped_gauge(cliff):
    """(TODO) Compute the clipped gauge of a stabilizer state.

    Args:
        cliff (numpy.ndarray): a Clifford matrix X|Z of shape (n_qubits, 2 * n_qubits + 1)
    
    Returns:
        A galois.FieldArray of shape (n_qubits, 2 * n_qubits) containing the stabilizer tableau in the clipped gauge.
    """
    tableau = GF(cliff)[:, :-1] # Discard parity bit
    n_qubits = tableau.shape[0]
    # Convert from X|Z to xz...xz, and standard order of qubits
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