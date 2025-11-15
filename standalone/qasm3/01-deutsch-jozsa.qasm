OPENQASM 3.0;
include "stdgates.inc"; 

// Deutsch-Jozsa Algorithm
qubit[4] q;
bit[3] c;
x q[3];

for int i in [0:3] {
    h q[i];
}

for int i in [0:2] {
    cx q[i], q[3];
}

for int i in [0:2] {
    h q[i];
}
// Measure the first three qubits into classical bits
//for int i in [0:2] {
//    c[i] = measure q[i];
//}
