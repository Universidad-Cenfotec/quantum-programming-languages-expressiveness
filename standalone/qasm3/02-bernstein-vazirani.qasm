OPENQASM 3.0;
include "stdgates.inc";
bit[4] c;
qubit[5] q;
x q[4];
h q[4];
for int i in [0:3] {
    h q[i];
}
cx q[0], q[4];
cx q[1], q[4];
cx q[3], q[4];
for int i in [0:3] {
    h q[i];
}
