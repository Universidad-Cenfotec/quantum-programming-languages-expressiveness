# Quantum Fourier Transform (QFT) in Qrisp
import qrisp as q
import numpy as np

def qft_qrisp(n):
    qv = q.QuantumVariable(n)
    
    # Apply QFT rotations
    for i in range(n):
        q.h(qv[i])
        for j in range(i+1, n):
            q.cp(np.pi / 2 ** (j-i), qv[j], qv[i])
    
    # Apply swaps to correct order
    for i in range(n//2):
        q.swap(qv[i], qv[n-i-1])
    
    return qv.qs.compile()

n = 6
qc = qft_qrisp(n)
print(qc)
