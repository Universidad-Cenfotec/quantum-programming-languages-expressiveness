import cirq
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import null_space

def simon_oracle_cirq(n, s):
    qubits = [cirq.LineQubit(i) for i in range(2 * n)]
    oracle = []
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            oracle.append(cirq.CX(qubits[i], qubits[n + i]))
    return oracle, qubits

def simon_algorithm_cirq(n, s):
    oracle, qubits = simon_oracle_cirq(n, s)
    circuit = cirq.Circuit()   
    circuit.append(cirq.H.on_each(*qubits[:n]))  
    circuit.append(oracle)   
    circuit.append(cirq.H.on_each(*qubits[:n]))   
    circuit.append(cirq.measure(*qubits[:n], key="result"))
    return circuit, qubits[:n]

def solve_simon_cirq(n, s, shots=1024):
    circuit = simon_algorithm_cirq(n, s)
    #simulator = cirq.Simulator()
    #result = simulator.run(circuit, repetitions=shots)
    #measurements = result.measurements["result"] 
    #equations = np.array(measurements) % 2
    #s_solution = null_space(equations).T[0] % 2
    #s_str = ''.join(str(int(bit)) for bit in s_solution)
    #return measurements, s_str, circuit
    return circuit

n = 3
s = "101"
circuit = solve_simon_cirq(n, s)
print(circuit)
