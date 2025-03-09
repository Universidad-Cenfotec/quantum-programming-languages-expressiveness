import qrisp

def deutsch_jozsa(n, oracle):
    # Deutsch-Jozsa algorithm for n-qubits
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
    # Constant oracle: does nothing """
    pass

def balanced_oracle(input_qubits, aux_qubit):
    # Balanced oracle: flips auxiliary qubit based on input
    for i in range(len(input_qubits)):
        qrisp.cx(input_qubits[i], aux_qubit)

n = 3
oracles = {"Constant": constant_oracle, "Balanced": balanced_oracle}
results = {}
for name, oracle in oracles.items():
    qc = deutsch_jozsa(n, oracle)
print(qc)