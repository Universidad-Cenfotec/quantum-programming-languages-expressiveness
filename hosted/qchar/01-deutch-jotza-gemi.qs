namespace DeutschJozsa {

    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    // Oráculos (Constant y Balanced)
    operation ConstantOracle(qubits : Qubit[]) : Unit is Adj + Ctl {
        // No hace nada (función constante)
    }

    operation BalancedOracle(qubits : Qubit[]) : Unit is Adj + Ctl {
        // Invierte el cúbito auxiliar basado en la entrada (función balanceada)
        let n = Length(qubits) - 1;
        for i in 0..n-1 {
            CNOT(qubits[i], qubits[n]);
        }
    }

    // Algoritmo Deutsch-Jozsa
    operation DeutschJozsaAlgorithm(n : Int, oracle : (Qubit[] => Unit is Adj + Ctl)) : Result[] {
        use qubits = Qubit[n + 1];

        // Inicialización
        X(qubits[n]);
        ApplyToEachA(H, qubits);

        // Oráculo
        oracle(qubits);

        // Transformada de Hadamard en los cúbits de entrada
        ApplyToEachA(H, qubits[0..n-1]);

        // Medición
        let results = MeasureEachZ(qubits[0..n-1]);

        ResetAll(qubits); // Reset los qubits antes de retornarlos.
        return results;
    }

    // Punto de entrada principal
    @EntryPoint()
    operation Main() : Unit {
        let n = 3;

        // Oráculo constante
        let constantResults = DeutschJozsaAlgorithm(n, ConstantOracle);
        Message($"Constant Oracle Results: {constantResults}");

        // Oráculo balanceado
        let balancedResults = DeutschJozsaAlgorithm(n, BalancedOracle);
        Message($"Balanced Oracle Results: {balancedResults}");
    }
}