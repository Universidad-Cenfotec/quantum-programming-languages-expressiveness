OPENQASM 3.0;
include "stdgates.inc";
bit[3] c;
qubit[4] q;
for int i in [0:2] {
    h q[i];
}
x q[1];
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q[1];
for int i in [0:2] {
    h q[i];
}
for int i in [0:2] {
    x q[i];
}
h q[2];
ccx q[0], q[1], q[2];
h q[2];
for int i in [0:2] {
    x q[i];
}
for int i in [0:2] {
    h q[i];
}
for int i in [0:2] {
    c[i] = measure q[i];
}
