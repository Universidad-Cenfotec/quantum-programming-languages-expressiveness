OPENQASM 3.0;
include "stdgates.inc";
gate cu1(p0) _gate_q_0, _gate_q_1 {
  u1(p0/2) _gate_q_0;
  cx _gate_q_0, _gate_q_1;
  u1(-p0/2) _gate_q_1;
  cx _gate_q_0, _gate_q_1;
  u1(p0/2) _gate_q_1;
}
bit[3] c;
qubit[4] q;
h q[0];
cu1(pi/2) q[1], q[0];
h q[1];
h q[2];
swap q[0], q[2];
for int i in [0:2] {
  h q[i];
  c[i] = measure q[i];
}
