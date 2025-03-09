import cirq
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import null_space

def simon_oracle_cirq(n, s):
    # simon algorithm oracle
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
    circuit, measure_qubits = simon_algorithm_cirq(n, s)
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    measurements = result.measurements["result"] 
    equations = np.array(measurements) % 2
    s_solution = null_space(equations).T[0] % 2
    s_str = ''.join(str(int(bit)) for bit in s_solution)

    return measurements, s_str, circuit


n = 3
s = "101"
counts, found_s, circuit = solve_simon_cirq(n, s)
print("\nCircuito de Simon en Cirq:")
print(circuit)
print("\nResultados de las mediciones:")
unique, counts = np.unique(counts, axis=0, return_counts=True)
counts_dict = {"".join(map(str, row)): count for row, count in zip(unique, counts)}
print(counts_dict)

print(f"\nEl valor secreto s encontrado es: {found_s}")


plt.bar(counts_dict.keys(), counts_dict.values(), color="blue")
plt.xlabel("Medidas")
plt.ylabel("Frecuencia")
plt.title("Resultados del Algoritmo de Simon en Cirq")
plt.xticks(rotation=45)
plt.show()