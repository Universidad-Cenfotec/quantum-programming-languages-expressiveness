namespace vazirani {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;

    operation  bernstein_vazirani(n : Int, s : Bool[]) : Result[] {
        use qubits = Qubit[n + 1];
        ApplyToEachA(H, qubits[0..n - 1]);
        X(qubits[n]);
        H(qubits[n]);
        for i in 0..n - 1 {
            Message($"numero: {n}");
            if (s[n - 1 - i]) {
                Controlled X([qubits[i]], qubits[n]);
            }
        }
        ApplyToEachA(H, qubits[0..n - 1]);
        let results = MeasureEachZ(qubits[0..n-1]);
        ResetAll(qubits);
        return results;
    }

    @EntryPoint()
    operation Main() : Unit {
        let n = 4;
        let s = [true,true, false, true]; 
        let constantResults = bernstein_vazirani(n, s);
        Message($"Constant Oracle Results: {constantResults}");
    }
}