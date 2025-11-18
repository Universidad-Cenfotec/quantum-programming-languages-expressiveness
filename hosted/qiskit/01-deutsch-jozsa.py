# Deutsch-Jozsa algorithm in Qiskit
from qiskit import QuantumCircuit

def deutsch_jozsa(n, oracle):
    qc = QuantumCircuit(n+1, n)
    qc.x(n)  
    qc.h(range(n + 1))
    qc.append(oracle, range(n + 1))
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def constant_oracle(n):
    oracle = QuantumCircuit(n + 1)
    return oracle.to_gate(label="Constant Oracle")

def balanced_oracle(n):
    oracle = QuantumCircuit(n + 1)
    for i in range(n):
        oracle.cx(i, n)  
    return oracle.to_gate(label="Balanced Oracle")

n = 3
qc = deutsch_jozsa(n, constant_oracle(n))
qc2 = deutsch_jozsa(n, balanced_oracle(n))
print(qc.draw("text"))
print(qc2.draw("text"))