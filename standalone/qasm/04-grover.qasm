OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[3];

// Step 1: Apply Hadamard gates to all qubits
h q[0];
h q[1];
h q[2];

// Step 2: Oracle for marked state "101"
// The oracle flips the amplitude of |101⟩ by applying X gates where the marked state is "0", then a controlled phase inversion on the entire state, and then the X gates are reversed.
x q[1];       // Flip q[1] because marked_state[1] is "0"
h q[2];       // Hadamard on the last qubit
ccx q[0], q[1], q[2];  // Controlled phase inversion (multi-controlled Toffoli)
h q[2];       // Reverse Hadamard
x q[1];       // Reverse flip q[1]

// Step 3: Diffusion operator
h q[0];
h q[1];
h q[2];
x q[0];
x q[1];
x q[2];
h q[2];
ccx q[0], q[1], q[2];  // Multi-controlled inversion
h q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];

// Step 4: Measure all qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
measure q[2] -> c[2];
