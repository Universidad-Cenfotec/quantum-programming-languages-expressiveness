namespace SimonAlgorithm {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arrays;

    operation SimonOracle(s : Bool[], qubits : Qubit[]) : Unit {
        let n = Length(s);
        for i in 0..n - 1 {
            if (s[n - 1 - i]) {
                Controlled X([qubits[i]], qubits[n + i]);
            }
        }
    }
    operation SimonAlgorithm(n : Int, s : Bool[]) : Result[] {
        use qubits = Qubit[2 * n];
        ApplyToEachA(H, qubits[0..n - 1]);
        SimonOracle(s, qubits);
        ApplyToEachA(H, qubits[0..n - 1]);
        let results = MeasureEachZ(qubits[0..n - 1]);
        ResetAll(qubits);
        return results;
    }
    
    // operation SimonSolver(n : Int, s : Bool[], shots : Int) : Unit {
    //    mutable resultsCount : (Result[], Int)[] = [];
    //    Message($"Resolviendo Simon con {shots} ejecuciones...");        
    //    for _ in 1 .. shots {
    //        let results = SimonAlgorithm(n, s);
    //        mutable found = false;
    //        for i in 0..Length(resultsCount) - 1 {
    //            let (existingString, existingCount) = resultsCount[i]; 
    //            if (existingString == results) {
    //                mutable newResultsCount = resultsCount;
    //                set newResultsCount w/= i <- (results, existingCount + 1);
    //                set resultsCount = newResultsCount;
    //                set found = true;                    
    //            }
    //        }
    //       if (not found) {
    //            set resultsCount += [(results, 1)];
    //        }
    //    }
    //    Message($"Conteo de resultados: {resultsCount}");
    //}

    @EntryPoint()
    operation Main() : Unit {
        let n = 3;
        let s = [true, false, true]; 
        //let shots = 100;
        //SimonSolver(n, s,shots);
        SimonAlgorithm(n, s);
    }
}