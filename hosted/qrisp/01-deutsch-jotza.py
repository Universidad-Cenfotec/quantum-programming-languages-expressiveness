import qrisp

def deutsch_jozsa(n, oracle):
    input_qubits = qrisp.QuantumVariable(n, name="input")
    aux_qubit = qrisp.QuantumVariable(1, name="aux")
    qrisp.x(aux_qubit)
    qrisp.h(input_qubits)
    qrisp.h(aux_qubit)
    oracle(input_qubits, aux_qubit)
    qrisp.h(input_qubits)
    qrisp.measure(input_qubits)
    return input_qubits.qs

def constant_oracle(input_qubits, aux_qubit):
    pass

def balanced_oracle(input_qubits, aux_qubit):
    for i in range(len(input_qubits)):
        qrisp.cx(input_qubits[i], aux_qubit)

n = 3
qc = deutsch_jozsa(n, constant_oracle)
qc1 = deutsch_jozsa(n, balanced_oracle)
print(qc)
print(qc1)
