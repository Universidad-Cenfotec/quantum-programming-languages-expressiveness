from qiskit import QuantumCircuit
import numpy as np

def qft_rotations(circuit, n):
    if n == 0:
        return
    n -= 1
    circuit.h(n)
    for qubit in range(n):
        circuit.cp(np.pi / 2 ** (n - qubit), qubit, n)
    qft_rotations(circuit, n)

def qft(n):
    circuit = QuantumCircuit(n)
    qft_rotations(circuit, n)
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit

n = 6
qc = qft(n)
print(qc.draw())
