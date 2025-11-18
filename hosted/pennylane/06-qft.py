# Quantum Fourier Transform (QFT) in Pennylane
import pennylane as qml
from pennylane import numpy as np

def qft(wires):
    n = len(wires)
    for i in range(n):
        qml.Hadamard(wires=wires[i])
        for j in range(i + 1, n):
            qml.ControlledPhaseShift(np.pi / 2 ** (j - i), wires=[wires[j], wires[i]])
    for i in range(n // 2):
        qml.SWAP(wires=[wires[i], wires[n - i - 1]])


n = 6
dev = qml.device('default.qubit', wires=n)
@qml.qnode(dev)
def circuit():
    qft(list(range(n)))
    return qml.state()
print(qml.draw(circuit)())
