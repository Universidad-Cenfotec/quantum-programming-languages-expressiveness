from qiskit.qasm3 import load
qc = load("../qasm/01-deutsch-jozsa.qasm")
qc.draw('mpl')