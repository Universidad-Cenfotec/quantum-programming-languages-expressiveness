// Deutsch-Jozsa Algorithm in QASM
OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg c[3];

// Initialize the auxiliary qubit to |1>
x q[3];

// Apply H gates on the first three qubits and the auxiliary qubit
h q[0];
h q[1];
h q[2];
h q[3];

// Balanced oracle: flips the auxiliary qubit based on the input
cx q[0], q[3];
cx q[1], q[3];
cx q[2], q[3];

// Apply H gates again on the first three qubits
h q[0];
h q[1];
h q[2];

// Measure the first three qubits into classical bits
// measure q[0] -> c[0];
// measure q[1] -> c[1];
// measure q[2] -> c[2];