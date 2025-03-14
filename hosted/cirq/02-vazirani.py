import cirq

def bernstein_vazirani_cirq(n, s):
    qubits = [cirq.LineQubit(i) for i in range(n + 1)]
    circuit = cirq.Circuit()
    circuit += [cirq.X(qubits[-1])]  
    circuit += cirq.H.on_each(*qubits)  
    circuit += cirq.Moment()
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit += cirq.CX(qubits[i], qubits[-1])
    circuit += cirq.H.on_each(*qubits[:-1])
    circuit += cirq.measure(*qubits[:-1], key="result")
    return circuit

n = 4
s = "1101"
circuit = bernstein_vazirani_cirq(n, s)
print(circuit)