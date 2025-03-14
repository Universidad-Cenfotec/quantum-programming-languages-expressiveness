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
    # Constant oracle: does nothing
    return cirq.Circuit() 

# Oracle  a balanced function (XOR of inputs)
def balanced_oracle(n):
    # Balanced oracle: flips auxiliary qubit based on input
    qubits = [cirq.LineQubit(i) for i in range(n)]
    aux_qubit = cirq.LineQubit(n)
    oracle = cirq.Circuit()
    for q in qubits:
        oracle.append(cirq.CNOT(q, aux_qubit))    
    return oracle

n = 3  
oracles = {"Constant": constant_oracle(n), "Balanced": balanced_oracle(n)}
results = {}
simulator = cirq.Simulator()

for name, oracle in oracles.items():
    circuit = deutsch_jozsa(n, oracle)
    result = simulator.run(circuit, repetitions=1024)
    # counts = dict(result.histogram(key="result"))
    # results[name] = counts
    # print(f"{name} Oracle Results:", counts)

print("Deutsch-Jozsa Circuit:")
print(deutsch_jozsa(n, balanced_oracle(n)))
