// Deutsch-Jozsa Algorithm in Q#
namespace DeutschJozsa {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    operation ConstantOracle(qubits : Qubit[]) : Unit is Adj + Ctl {
    }

    operation BalancedOracle(qubits : Qubit[]) : Unit is Adj + Ctl {
        let n = Length(qubits) - 1;
        for i in 0..n-1 {
            CNOT(qubits[i], qubits[n]);
        }
    }


    operation DeutschJozsaAlgorithm() : Unit {
        use qubits = Qubit[n + 1];
        X(qubits[n]);
        ApplyToEachA(H, qubits);
        oracle(qubits);
        ApplyToEachA(H, qubits[0..n-1]);
        let results = MeasureEachZ(qubits[0..n-1]);
        ResetAll(qubits);
        return results;
    }

     @EntryPoint()
    operation Main() : Unit {
        let n = 3;
        let constantResults = DeutschJozsaAlgorithm(n, ConstantOracle);
        Message($"Constant Oracle Results: {constantResults}");
        let balancedResults = DeutschJozsaAlgorithm(n, BalancedOracle);
        Message($"Balanced Oracle Results: {balancedResults}");
    }
}