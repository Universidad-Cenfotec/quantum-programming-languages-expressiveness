import cirq

def deutsch_jozsa(n, oracle):
    qubits = [cirq.LineQubit(i) for i in range(n)]  
    aux_qubit = cirq.LineQubit(n)    
    circuit = cirq.Circuit()
    circuit.append(cirq.X(aux_qubit))
    circuit.append(cirq.H(q) for q in qubits + [aux_qubit])
    circuit.append(oracle)
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key="result"))
    return circuit

def constant_oracle(n):
    return cirq.Circuit() 

def balanced_oracle(n):
    qubits = [cirq.LineQubit(i) for i in range(n)]
    aux_qubit = cirq.LineQubit(n)
    oracle = cirq.Circuit()
    for q in qubits:
        oracle.append(cirq.CNOT(q, aux_qubit))    
    return oracle

n = 3
print(deutsch_jozsa(n, balanced_oracle(n)))
print(deutsch_jozsa(n, constant_oracle(n)))