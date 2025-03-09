OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];
creg c[3];

// Step 1: Apply Hadamard gates to the input qubits
h q[0];
h q[1];
h q[2];

// Step 2: Simon Oracle for s = "101"
// This is a hand-coded example of an oracle where s = "101"
// If s[i] = "1", we apply CX from q[i] to q[n+i].
cx q[0], q[3];
cx q[2], q[5];

// Step 3: Apply Hadamard gates again to the input qubits
h q[0];
h q[1];
h q[2];

// Step 4: Measure the input qubits into the classical register
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
