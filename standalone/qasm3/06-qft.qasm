// Quantum Fourier Transform (QFT) in OpenQASM 3.0 for 6 qubits
OPENQASM 3.0;
include "stdgates.inc";

// Using a subroutine for QFT
def qft(qubit[6] q) {
    h q[0];
    cu1(pi/2) q[1], q[0];
    cu1(pi/4) q[2], q[0];
    cu1(pi/8) q[3], q[0];
    cu1(pi/16) q[4], q[0];
    cu1(pi/32) q[5], q[0];

    h q[1];
    cu1(pi/2) q[2], q[1];
    cu1(pi/4) q[3], q[1];
    cu1(pi/8) q[4], q[1];
    cu1(pi/16) q[5], q[1];

    h q[2];
    cu1(pi/2) q[3], q[2];
    cu1(pi/4) q[4], q[2];
    cu1(pi/8) q[5], q[2];

    h q[3];
    cu1(pi/2) q[4], q[3];
    cu1(pi/4) q[5], q[3];

    h q[4];
    cu1(pi/2) q[5], q[4];

    h q[5];

    swap q[0], q[5];
    swap q[1], q[4];
    swap q[2], q[3];
}

qubit[6] q;
bit[6] c;

// Apply QFT
qft(q);

// Measure all qubits
//c = measure q;
