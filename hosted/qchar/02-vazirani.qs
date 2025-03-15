namespace vazirani {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation  bernstein_vazirani(n : Int, s : Bool[]) : Result[] {
        use qubits = Qubit[n + 1];
        ApplyToEachA(H, qubits[0..n - 1]);
        X(qubits[n]);
        H(qubits[n]);
        // oracle
        
         for i in 0..n - 1 {
            Message($"numero: {n}");
            if (s[n - 1 - i]) {
                Controlled X([qubits[i]], qubits[n]);
            }
        }

        ApplyToEachA(H, qubits[0..n - 1]);
        // Medición
        let results = MeasureEachZ(qubits[0..n-1]);

        ResetAll(qubits); // Reset los qubits antes de retornarlos.
        return results;

    }


    @EntryPoint()
    operation Main() : Unit {
        let n = 4;
        let s = [true,true, false, true]; // Representación del string "1101" en binario
        
        let constantResults = bernstein_vazirani(n, s);
        Message($"Constant Oracle Results: {constantResults}");
    }
}