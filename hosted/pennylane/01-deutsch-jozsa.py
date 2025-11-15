# Quantum Deutsch-Jozsa Algorithm in Pennylane
import pennylane as qml 
from pennylane import numpy as np


def applyHadamard(n):
    for i in range(n):
        qml.Hadamard(wires=i)

def deutsch_jozsa(n, oracle):
    dev = qml.device('default.qubit', wires=n+1)
    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            pass
        qml.PauliX(wires=n)
        applyHadamard(n+1)
        oracle()
        applyHadamard(n)        
        return qml.sample(wires=range(n))
    return circuit

def constant_oracle():
    def _oracle():
        pass
    return _oracle

def balanced_oracle(n):
    def _oracle():
        for i in range(n):
            qml.CNOT(wires=[i, n])
    return _oracle

n = 3
print(qml.draw( deutsch_jozsa(n, balanced_oracle(n)))())
print(qml.draw(deutsch_jozsa(n,  constant_oracle()))())
