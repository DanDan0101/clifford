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
    L = N // D

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
    L = circ.N // D
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

def entropy(state, D = 1, A = None, log2 = False):
    """Calculates the bipartite entanglement entropy of the state.

    Args:
        state (pc.stabilizer.StabilizerState): The state to calculate the entropy of.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        A (list, optional): The list of qudit positions to calculate the entropy of. Defaults to None (first half of the qudits)
        log2 (bool, optional): Whether to return the entropy in base e or base 2. Defaults to False.
        
    Returns:
        float: The bipartite entanglement entropy.
    """
    N = state.N
    L = N // D
    if A is None:
        A = [i for i in range(L // 2)]
    entropy_log2 = state.entropy([j for i in A for j in qubit_pos(i, D)])
    if log2:
        return entropy_log2
    else:
        return entropy_log2 * np.log(2)

def bip_info(state, D = 1, recip_size = 8):
    """Calculates the bipartite mutual information of two opposite subsystems.

    Args:
        state (pc.stabilizer.StabilizerState): The state to calculate the mutual information of.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        recip_size (int, optional): The reciprocal size of the subsystems, in terms of L. Defaults to 8.
    
    Returns:
        float: The bipartite mutual information.
    """
    N = state.N
    L = N // D
    assert recip_size > 2
    subsys_size = L // recip_size
    subsys_1 = [i for i in range(subsys_size)]
    subsys_2 = [L // 2 + i for i in range(subsys_size)]
    return entropy(state, D, subsys_1) + entropy(state, D, subsys_2) - entropy(state, D, subsys_1 + subsys_2)

def trip_info(state, D = 1, recip_size = 4):
    """Calculates the negative tripartite mutual information of three adjacent subsystems.
    
    Args:
        state (pc.stabilizer.StabilizerState): The state to calculate the mutual information of.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        recip_size (int, optional): The reciprocal size of the subsystems, in terms of L. Defaults to 4.
    
    Returns:
        float: The negative tripartite mutual information.
    """
    N = state.N
    L = N // D
    assert recip_size > 3

    subsys_size = int(L / recip_size)
    subsys_1 = [i for i in range(subsys_size)]
    subsys_2 = [i + subsys_size for i in range(subsys_size)]
    subsys_3 = [i + 2 * subsys_size for i in range(subsys_size)]

    info_1 = entropy(state, D, subsys_1) + entropy(state, D, subsys_2) + entropy(state, D, subsys_3)
    info_2 = entropy(state, D, subsys_1 + subsys_2) + entropy(state, D, subsys_2 + subsys_3) + entropy(state, D, subsys_3 + subsys_1)
    info_3 = entropy(state, D, subsys_1 + subsys_2 + subsys_3)
    return -info_1 + info_2 - info_3

def sample(f, L, p, D = 1, timesteps = 128, depth = None):
    """
    Samples a function f from a stabilizer state.

    Args:
        f (function): The function to sample. Takes a pc.stabilizer.StabilizerState as input and returns a float.
        L (int): The number of qudits in the state.
        p (float): The probability of measuring each qudit.
        D (int, optional): The number of qubits per qudit. Defaults to 1.
        timesteps (int, optional): The number of timesteps to sample for. Defaults to 128.
        depth (int, optional): The initial depth of the circuit. Defaults to None (L // 2).
    Returns:
        float: mean of f over the samples.
        float: mean of f^2 over the samples.
    """
    N = L * D
    state = pc.zero_state(N)
    if depth is None:
        depth = L // 2
    circ = create_circuit(L, depth, p, D)
    circ.forward(state)
    samples = np.zeros(timesteps)
    parity = True

    for i in range(timesteps):
        samples[i] = f(state)
        circ = pc.circuit.Circuit(N)
        if parity:
            random_clifford(circ, even = True, D = D)
        else:
            random_clifford(circ, even = False, D = D)
        if p > 0:
            random_measurement(circ, p, D)
        circ.forward(state)
        parity = not parity
    return np.mean(samples), np.mean(samples**2)

@njit
def xi(L, z1, z2):
    """Calculates xi, as defined by Li et al. in https://arxiv.org/abs/2003.12721.

    Args:
        L (int): The number of qudits in the state.
        z1 (int): The first qudit position.
        z2 (int): The second qudit position.

    Returns:
        float: xi.
    """
    if z1 == z2:
        raise ValueError("z1 and z2 must be different")
    return (np.pi / L / np.sin(np.pi * (z1 - z2) / L)) ** 2
