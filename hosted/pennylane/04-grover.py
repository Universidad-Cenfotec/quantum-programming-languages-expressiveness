import pennylane as qml
from pennylane import numpy as np

def applyHadamard(n):
    for i in n:
        qml.Hadamard(wires=i)

def applyPauliX(n):
    for i in n:
        qml.PauliX(wires=i)

def grover_oracle(wires, marked_state):
    def _oracle():
        for i, bit in enumerate(marked_state):
            if bit == '0':
                qml.PauliX(wires=wires[i])
        control_values = [1] * (len(wires) - 1)
        qml.MultiControlledX(wires=wires, control_values=control_values)
        for i, bit in enumerate(marked_state):
            if bit == '0':
                qml.PauliX(wires=wires[i])
    return _oracle

def grover_diffusion(wires):
    def _diffusion():
        applyHadamard(wires)
        applyPauliX(wires)
        control_values = [1] * (len(wires) - 1)
        qml.MultiControlledX(wires=wires, control_values=control_values)
        applyPauliX(wires)
        applyHadamard(wires)
    return _diffusion

def grover_algorithm(n, marked_state, iterations=1):
    dev = qml.device('default.qubit', wires=n)
    wires = list(range(n))
    oracle = grover_oracle(wires, marked_state)
    diffusion = grover_diffusion(wires)
    @qml.qnode(dev)
    def circuit():
        applyHadamard(wires)
        for _ in range(iterations):
            oracle()
            diffusion()
        return qml.sample(wires=wires)
    return circuit

n = 3
marked_state = "101"
iterations = int(np.pi / 4 * np.sqrt(2**n))
circ = grover_algorithm(n, marked_state, iterations)
print(qml.draw(circ)())
