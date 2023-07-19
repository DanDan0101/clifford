import numpy as np
import pyclifford as pc
from numba import njit
from tqdm import tqdm

def random_clifford(circ, even = True):
    """Adds a layer of random Clifford gates to the circuit.

    Args:
        circ (pc.circuit.Circuit): The circuit to add gates to.
        even (bool, optional): Whether to add gates starting with even or odd qubits. Defaults to True.
    
    Returns:
        pc.circuit.Circuit: The circuit with gates added.
    """
    for i in range(circ.N // 2):
        if even:
            circ.gate(2*i, 2*i + 1)
        else:
            circ.gate(2*i + 1, (2*i + 2) % circ.N)
    return circ

@njit
def generate_measurement_position(N, p):
    """Generates a random list of positions to measure.

    Args:
        N (int): The number of qubits in the circuit.
        p (float): The probability of measuring each qubit.

    Returns:
        list: The list of positions to measure.
    """
    positions = []
    for i in range(N):
        if np.random.rand()<p:
            positions.append(i)
    return positions

def random_measurement(circ, p):
    """Adds a layer of random measurements to the circuit.

    Args:
        circ (pc.circuit.Circuit): The circuit to add measurements to.
        p (float): The probability of measuring each qubit.

    Returns:
        pc.circuit.Circuit: The circuit with measurements added.
    """
    pos = generate_measurement_position(circ.N, p)
    if pos: # not empty
        circ.measure(*pos)
    return circ

def create_circuit(N, depth, p):
    """Creates a random Clifford circuit with random measurements.
    
    Args:
        N (int): The number of qubits in the circuit.
        depth (int): The number of time steps in the circuit.
        p (float): The probability of measuring each qubit.
    
    Returns:
        pc.circuit.Circuit: The random Clifford circuit.
    """
    if p > 0:
        circ = pc.circuit.Circuit(N)
        for i in range(depth):
            circ = random_clifford(circ, even = True)
            circ = random_measurement(circ, p)
            circ = random_clifford(circ, even = False)
            circ = random_measurement(circ, p)
    else:
        circ = pc.circuit.CliffordCircuit(N)
        for i in range(depth):
            circ = random_clifford(circ, even = True)
            circ = random_clifford(circ, even = False)
    return circ

def me_state(N):
    """Creates a random maximally entangled state.

    Args:
        N (int): The number of qubits in the state.
    
    Returns:
        pc.stabilizer.StabilizerState: The maximally entangled state.
    """
    state = pc.zero_state(N)
    circ = create_circuit(N, N // 2, 0)
    state = circ.forward(state)
    return state

def entropy(state):
    """Calculates the bipartite entanglement entropy of the state.

    Args:
        state (pc.stabilizer.StabilizerState): The state to calculate the entropy of.

    Returns:
        float: The bipartite entanglement entropy.
    """
    return state.entropy([i for i in range(state.N//2)])

def evolve_entropy(state, depth, p):
    """Computes the bipartite entanglement entropy of the state under random time evolution.

    Args:
        state (pc.stabilizer.StabilizerState): The initial state.
        depth (int): The number of time steps.
        p (float): The probability of measuring each qubit.

    Returns:
        np.ndarray: An array of shape (depth + 1,) containing the bipartite entanglement entropies.
    """
    entropies = [entropy(state)]
    for _ in range(depth):
        circ = create_circuit(state.N, 1, p)
        state = circ.forward(state)
        entropies.append(entropy(state))
    return np.array(entropies)

def evolve_entropies(state, depth, p, shots = 10, logging = True):
    """Computes an ensemble average version of evolve_entropy.

    Args:
        state (pc.stabilizer.StabilizerState): The initial state.
        depth (int): The number of time steps.
        p (float): The probability of measuring each qubit.
        shots (int, optional): The number of samples to average over. Defaults to 10.
        logging (bool, optional): Whether to display a progress bar. Defaults to True.
    
    Returns:
        np.ndarray: An array of shape (2, depth + 1) containing the mean and std of the bipartite entanglement entropies.
    """
    if logging:
        entropies_raw = np.array([evolve_entropy(state, depth, p) for _ in tqdm(range(shots))])
    else:
        entropies_raw = np.array([evolve_entropy(state, depth, p) for _ in range(shots)])
    entropies_mean = np.mean(entropies_raw, axis = 0)
    entropies_std = np.std(entropies_raw, axis = 0, ddof = 1) / np.sqrt(shots)
    return np.array([entropies_mean, entropies_std])
