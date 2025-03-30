from qiskit import QuantumCircuit

def bernstein_vazirani(n, s):
    qc = QuantumCircuit(n + 1, n) 
    qc.x(n)
    qc.h(range(n + 1))
    for i, bit in enumerate(reversed(s)):  
        if bit == "1":
            qc.cx(i, n)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

n = 4 
s = "1101" 
qc = bernstein_vazirani(n, s)
print(qc.draw("text"))