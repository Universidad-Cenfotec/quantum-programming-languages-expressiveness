OPENQASM 3.0;
include "stdgates.inc";
bit[3] c;
qubit[6] q;
for int i in [0:2] {
    h q[i];
}
cx q[0], q[3];
cx q[2], q[5];
for int i in [0:2] {
    h q[i];
}
