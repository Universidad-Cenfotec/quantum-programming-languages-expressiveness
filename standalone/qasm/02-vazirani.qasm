OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[4];

// Initialize the auxiliary qubit
x q[4];
h q[4];

// Apply Hadamard gates to all input qubits
h q[0];
h q[1];
h q[2];
h q[3];

// Apply CNOT gates based on the secret string s = "1101"
// For "1101" (reversed), this means:
// - bit 1 (q[0]) and bit 2 (q[1]) are connected to q[4] with CNOT
// - bit 4 (q[3]) is connected to q[4] with CNOT
cx q[0], q[4];
cx q[1], q[4];
cx q[3], q[4];

// Apply a barrier (optional in OpenQASM, just for clarity)
// -- OpenQASM 2.0 doesn’t have a barrier instruction, so you can just leave this out or add a comment
// barrier q;

// Apply Hadamard gates to all input qubits again
h q[0];
h q[1];
h q[2];
h q[3];

// Barrier again (optional)
// -- Same note as above regarding barriers

// Measure the input qubits into classical registers
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
