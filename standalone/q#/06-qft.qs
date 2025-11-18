// Quantum Fourier Transform (QFT) in Q#
namespace QFT {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    operation QFT(nQubits : Int) : Unit {
        use qs = Qubit[nQubits];
        for i in 0 .. nQubits - 1 {
            H(qs[i]);
            for j in i+1 .. nQubits - 1 {
                (Controlled R1Frac)([qs[j]], (1, 2^(j-i), qs[i]));
            }
        }
        // Reverse the order of the qubits using SWAP gates
        for i in 0 .. (nQubits / 2 - 1) {
            SWAP(qs[i], qs[nQubits - i - 1]);
        }
        ResetAll(qs);
    }

    @EntryPoint()
    operation RunQFT() : Unit {
        // Ejecuta QFT con 6 qubits
        QFT(6);
    }
}
