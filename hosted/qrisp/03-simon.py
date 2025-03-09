import qrisp

def simon_oracle_qrisp(n, s):
    # Simon Oracle para el algoritmo de Simon en QRISP
    qc = qrisp.QuantumCircuit(2 * n)
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(i, n + i)
    return qc.to_gate()  

def simon_algorithm_qrisp(n, s):
    # Implementación del algoritmo de Simon en QRISP
    qc = qrisp.QuantumCircuit(2 * n, n)
    qc.h(range(n))    
    # Apply oracle
    oracle = simon_oracle_qrisp(n, s)
    qc.append(oracle, range(2 * n))
    qc.h(range(n))
    qc.measure(range(n), range(n))    
    return qc

n = 3
s = "101"
qc = simon_algorithm_qrisp(n, s)
print(qc)