import qrisp

def bernstein_vazirani_qrisp(n, s):
    qc = qrisp.QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(i, n)    
    # qc.barrier() 
    qc.h(range(n))
    # qc.barrier()
    qc.measure(range(n), range(n))
    return qc

n = 4 
s = "1101" 
qc = bernstein_vazirani_qrisp(n, s)
print(qc)