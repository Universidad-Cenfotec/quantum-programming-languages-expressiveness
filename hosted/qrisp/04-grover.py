import qrisp

def grover_oracle_qrisp(n, marked_state):    
    oracle = qrisp.QuantumCircuit(n)
    for i, bit in enumerate(reversed(marked_state)):
        if bit == '0':
            oracle.x(i)
    oracle.h(n - 1)
    oracle.mcx(list(range(n - 1)), n - 1)
    oracle.h(n - 1)

    for i, bit in enumerate(reversed(marked_state)):
        if bit == '0':
            oracle.x(i)
    return oracle.to_gate()

def grover_diffusion_qrisp(n):    
    diffusion = qrisp.QuantumCircuit(n)
    diffusion.h(range(n))
    diffusion.x(range(n))
    diffusion.h(n - 1)
    diffusion.mcx(list(range(n - 1)), n - 1)
    diffusion.h(n - 1)
    diffusion.x(range(n))
    diffusion.h(range(n))
    return diffusion.to_gate()

def grover_algorithm_qrisp(n, marked_state, iterations=1):  
    qc = qrisp.QuantumCircuit(n, n)
    qc.h(range(n))
    oracle = grover_oracle_qrisp(n, marked_state)
    diffusion = grover_diffusion_qrisp(n)
    for _ in range(iterations):
        qc.append(oracle, range(n))
        qc.append(diffusion, range(n))
    qc.measure(range(n), range(n))
    return qc

n = 3
marked_state = "101"
iterations = int(np.pi / 4 * np.sqrt(2**n)) 
qc = grover_algorithm_qrisp(n, marked_state, iterations)
print(qc)
