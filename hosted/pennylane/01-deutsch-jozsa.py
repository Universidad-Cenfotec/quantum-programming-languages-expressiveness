# Quantum Deutsch-Jozsa Algorithm in Pennylane
import pennylane as qml
from pennylane import numpy as np

def deutsch_jozsa(n, oracle):
    dev = qml.device('default.qubit', wires=n+1)

    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            pass
        qml.PauliX(wires=n)
        for i in range(n+1):
            qml.Hadamard(wires=i)
        oracle()
        for i in range(n):
            qml.Hadamard(wires=i)
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
print('Balanced')
circ_bal = deutsch_jozsa(n, balanced_oracle(n))
print(qml.draw(circ_bal)())
print('Constant')
circ_const = deutsch_jozsa(n,  constant_oracle())
print(qml.draw(circ_const)())
