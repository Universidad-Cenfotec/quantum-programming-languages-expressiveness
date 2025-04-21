import qrisp
def oracle(qv, s):
    for i in range(len(s)):
        if s[i] == "1":
            qrisp.cx(qv[i], qv[n + i])
def simon_algorithm_qrisp(n, s):
    qv = qrisp.QuantumVariable(2*n)
    with qrisp.conjugate(qrisp.h)(qv[:n]):
        oracle(qv, s)
    return qv.qs.compile()
n = 3
s = "101"
qc = simon_algorithm_qrisp(n, s)
print(qc)