import pennylane as qml
from pennylane import numpy as np

def applyHadamard(n):
    for i in range(n):
        qml.Hadamard(wires=i)

def bernstein_vazirani(n, s):
    dev = qml.device('default.qubit', wires=n+1)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        applyHadamard(n+1)
        for i, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[i, n])
        applyHadamard(n)
        return qml.sample(wires=range(n))
    return circuit

n = 4
s = "1101"
circ = bernstein_vazirani(n, s)
print(qml.draw(circ)())
