# Quantum Fourier Transform (QFT) in Cirq
import cirq
import numpy as np

def qft_circuit(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    circuit = cirq.Circuit()
    for i in range(n):
        circuit.append(cirq.H(qubits[i]))
        for j in range(i+1, n):
            angle = np.pi/2 ** (j-i)
            circuit.append(cirq.CZPowGate(exponent=angle/np.pi)(qubits[j], qubits[i]))
    for i in range(n//2):
        circuit.append(cirq.SWAP(qubits[i], qubits[n-i-1]))
    return circuit

n = 6
qc = qft_circuit(n)
print(qc)
