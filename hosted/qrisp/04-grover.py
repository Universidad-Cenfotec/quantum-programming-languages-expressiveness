import qrisp
import numpy as np
n = 3
marked_state = "101"
iterations = int(np.pi / 4 * np.sqrt(2**n)) 
qv = qrisp.QuantumVariable(n)
oracle = lambda qv : qrisp.mcz(qv, ctrl_state = marked_state)
qrisp.grover.grovers_alg(qv, oracle)
# qc = qv.qs.compile()
# print(qc)
