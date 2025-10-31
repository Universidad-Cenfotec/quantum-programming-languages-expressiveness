OPENQASM 3.0;
include "stdgates.inc";

// Deutsch-Jozsa Algorithm
qubit[4] q;
bit[3] c;

// Apply H gates on all qubits
for int i in [0:3] {
    h q[i];
}

// Balanced oracle: flips the auxiliary qubit based on input
for int i in [0:2] {
    cx q[i], q[3];
}

// Apply H gates again on the first three qubits
for int i in [0:2] {
    h q[i];
}

// Measure the first three qubits into classical bits
//for int i in [0:2] {
//    c[i] = measure q[i];
//}
