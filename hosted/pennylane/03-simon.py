import pennylane as qml

def applyHadamard(n):
    for i in range(n):
        qml.Hadamard(wires=i)

def simon_oracle(n, s):
    def _oracle():
        for i, bit in enumerate(reversed(s)):
            if bit == '1':
                qml.CNOT(wires=[i, n + i])
    return _oracle

def simon_algorithm(n, s):
    dev = qml.device('default.qubit', wires=2 * n)
    oracle = simon_oracle(n, s)
    @qml.qnode(dev)
    def circuit():
        applyHadamard(n)
        oracle()
        applyHadamard(n)
        return qml.sample(wires=range(n))
    return circuit

n = 3
s = "101"
circ = simon_algorithm(n, s)
print(qml.draw(circ)())
