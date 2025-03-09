import cirq
import numpy as np
import matplotlib.pyplot as plt

def grover_oracle(qubits, marked_state):
    oracle = cirq.Circuit()    
    for i, bit in enumerate(marked_state):
        if bit == '0':
            oracle.append(cirq.X(qubits[i]))
    
    oracle.append(cirq.H(qubits[-1]))
    oracle.append(cirq.TOFFOLI(qubits[0], qubits[1], qubits[2]))
    oracle.append(cirq.H(qubits[-1]))
    
    for i, bit in enumerate(marked_state):
        if bit == '0':
            oracle.append(cirq.X(qubits[i]))    
    return oracle

def grover_diffusion(qubits):
    diffusion = cirq.Circuit()
    diffusion.append(cirq.H.on_each(*qubits))
    diffusion.append(cirq.X.on_each(*qubits))    
    diffusion.append(cirq.H(qubits[-1]))
    diffusion.append(cirq.TOFFOLI(qubits[0], qubits[1], qubits[2]))
    diffusion.append(cirq.H(qubits[-1]))    
    diffusion.append(cirq.X.on_each(*qubits))
    diffusion.append(cirq.H.on_each(*qubits))    
    return diffusion

def grover_algorithm(n, marked_state, iterations=1):
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()    
    circuit.append(cirq.H.on_each(*qubits))    
    oracle = grover_oracle(qubits, marked_state)
    diffusion = grover_diffusion(qubits)
    
    for _ in range(iterations):
        circuit.append(oracle)
        circuit.append(diffusion)    
    circuit.append(cirq.measure(*qubits, key='result'))    
    return circuit, qubits

def run_grover(n, marked_state, shots=1024):
    """Ejecuta el algoritmo de Grover y muestra los resultados"""
    iterations = int(np.pi / 4 * np.sqrt(2**n))
    circuit, qubits = grover_algorithm(n, marked_state, iterations)
    
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=shots)
    counts = result.histogram(key='result')
    formatted_counts = {format(key, f'0{n}b'): value for key, value in sorted(counts.items())}    
    return formatted_counts, circuit

def plot_histogram(counts):
    """Grafica un histograma de los resultados"""
    sorted_keys = sorted(counts.keys())
    sorted_values = [counts[key] for key in sorted_keys]    
    plt.bar(sorted_keys, sorted_values)
    plt.xlabel("State (binary)")
    plt.ylabel("Frequency")
    plt.title("Grover results")
    plt.xticks(rotation=90)
    plt.show()

n = 3
marked_state = "101"
counts, circuit = run_grover(n, marked_state)
print("\nResultados de las mediciones:")
print(counts)
print("\nCircuito:")
print(circuit)
plot_histogram(counts)