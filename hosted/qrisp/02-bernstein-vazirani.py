import qrisp
def bernstein_vazirani_qrisp(n, s):
    qv = qrisp.QuantumVariable(n+1)
    qrisp.x(qv[-1])
    with qrisp.conjugate(qrisp.h)(qv):
        for i in range(len(s)):
            if s[i] == "1":
                qrisp.cx(qv[i], qv[n])
    qrisp.measure(qv)
    return qv.qs.compile()
n = 4 
s = "1101" 
qc = bernstein_vazirani_qrisp(n, s)
print(qc)