import numpy as np
import pyclifford as pc
from numba import njit
from tqdm import tqdm

@njit
def qubit_pos(i, D = 1):
    """Generates a list of qubit positions corresponding to qudit i.

    Args:
        i (int): The qudit position.
        D (int, optional): The number of qubits per qudit. Defaults to 1.

    Returns:
        list: The list of qubit positions.
    """
    return [i * D + j for j in range(D)]

def random_clifford(circ, even = True, D = 1):
    """Adds a layer of random Clifford gates to the circuit.

    Args:
        circ (pc.circuit.Circuit): The circuit to add gates to.
        even (bool, optional): Whether to add gates starting with even or odd qudits. Defaults to True.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
    
    Returns:
        None
    """
    N = circ.N
    assert N % D == 0
    L = int(N / D)

    for i in range(L // 2):
        if even:
            q1 = 2 * i
            q2 = q1 + 1
        else:
            q1 = 2 * i + 1
            q2 = (q1 + 1) % L
        circ.gate(*qubit_pos(q1, D), *qubit_pos(q2, D))

@njit
def generate_measurement_position(L, p, D = 1):
    """Generates a random list of positions to measure.

    Args:
        L (int): The number of qudits in the circuit.
        p (float): The probability of measuring each qudit.
        D (int, optional): The number of qubits per qudit. Defaults to 1.

    Returns:
        list: The list of qubit positions to measure.
    """
    positions = []
    for i in range(L):
        if np.random.rand()<p:
            positions.extend(qubit_pos(i, D))
    return positions

def random_measurement(circ, p, D = 1):
    """Adds a layer of random measurements to the circuit.

    Args:
        circ (pc.circuit.Circuit): The circuit to add measurements to.
        p (float): The probability of measuring each qudit.
        D (int, optional): The number of qubits per qudit. Defaults to 1.

    Returns:
        None
    """
    L = int(circ.N / D)
    pos = generate_measurement_position(L, p, D)
    if pos: # not empty
        circ.measure(*pos)

def create_circuit(L, depth, p, D = 1):
    """Creates a random Clifford circuit with random measurements.
    
    Args:
        L (int): The number of qudits in the circuit.
        depth (int): The number of time steps in the circuit.
        p (float): The probability of measuring each qudit.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
    
    Returns:
        pc.circuit.Circuit: The random Clifford circuit.
    """
    N = L * D
    if p > 0:
        circ = pc.circuit.Circuit(N)
        for _ in range(depth):
            random_clifford(circ, even = True, D = D)
            random_measurement(circ, p, D)
            random_clifford(circ, even = False, D = D)
            random_measurement(circ, p, D)
    else:
        circ = pc.circuit.Circuit(N) # TODO: use tc.circuit.CliffordCircuit for greater speedup
        for _ in range(depth):
            random_clifford(circ, even = True, D = D)
            random_clifford(circ, even = False, D = D)
    return circ

def me_state(L, D = 1):
    """Creates a random maximally entangled state.

    Args:
        L (int): The number of qudits in the state.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
    
    Returns:
        pc.stabilizer.StabilizerState: The maximally entangled state.
    """
    N = L * D
    state = pc.zero_state(N)
    circ = create_circuit(L, L // 2, 0, D)
    circ.forward(state)
    return state

def entropy(state, D = 1, A = None):
    """Calculates the bipartite entanglement entropy of the state.

    Args:
        state (pc.stabilizer.StabilizerState): The state to calculate the entropy of.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        A (list, optional): The list of qudit positions to calculate the entropy of. Defaults to None (first half of the qudits)

    Returns:
        float: The bipartite entanglement entropy.
    """
    N = state.N
    L = int(N / D)
    if A is None:
        A = [i for i in range(L // 2)]
    return state.entropy([j for i in A for j in qubit_pos(i, D)])

def evolve_entropy(state, depth, p, D = 1):
    """Computes the bipartite entanglement entropy of the state under random time evolution.

    Args:
        state (pc.stabilizer.StabilizerState): The initial state.
        depth (int): The number of time steps.
        p (float): The probability of measuring each qudit.
        D (int, optional): The number of qubits per qudit. Defaults to 1.

    Returns:
        np.ndarray: An array of shape (depth + 1,) containing the bipartite entanglement entropies.
    """
    N = state.N
    L = int(N / D)
    entropies = [entropy(state, D)]
    for _ in range(depth):
        circ = create_circuit(L, 1, p, D)
        circ.forward(state)
        entropies.append(entropy(state, D))
    return np.array(entropies)

def evolve_entropies(L, depth, p, zero = True, shots = 10, D = 1, logging = True):
    """Computes an ensemble average version of evolve_entropy.

    Args:
        L (int): The number of qudits in the state.
        depth (int): The number of time steps.
        p (float): The probability of measuring each qudit.
        zero (bool, optional): Whether to start from the zero state. Defaults to True.
        shots (int, optional): The number of samples to average over. Defaults to 10.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        logging (bool, optional): Whether to display a progress bar. Defaults to True.
    
    Returns:
        np.ndarray: An array of shape (2, depth + 1) containing the mean and std of the bipartite entanglement entropies.
    """
    N = L * D
    entropies_raw = []
    if logging:
        for _ in tqdm(range(shots)):
            if zero:
                state = pc.zero_state(N)
            else:
                state = me_state(L, D)
            entropies_raw.append(evolve_entropy(state, depth, p, D))
    else:
        for _ in range(shots):
            if zero:
                state = pc.zero_state(N)
            else:
                state = me_state(L, D)
            entropies_raw.append(evolve_entropy(state, depth, p, D))
    
    entropies_raw = np.array(entropies_raw)
    entropies_mean = np.mean(entropies_raw, axis = 0)
    entropies_std = np.std(entropies_raw, axis = 0, ddof = 1) / np.sqrt(shots)
    return np.array([entropies_mean, entropies_std])
