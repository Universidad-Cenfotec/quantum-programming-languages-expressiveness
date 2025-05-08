import qrisp
n = 3
marked_state = "101"
qv = qrisp.QuantumVariable(n)
oracle = lambda qv : qrisp.mcz(qv, ctrl_state=marked_state)
qrisp.grover.grovers_alg(qv, oracle)
qc = qv.qs.compile()
print(qc)
