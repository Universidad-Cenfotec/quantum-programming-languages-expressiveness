namespace GroverAlgorithm {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    operation GroverOracle(qubits : Qubit[], markedState : Bool[]) : Unit is Adj{
        let n = Length(qubits);
        for i in 0..n - 1 {
            if (not markedState[n - 1 - i]) {
                X(qubits[i]);
            }
        }
        H(qubits[n - 1]);
        Controlled X(Most(qubits), qubits[n - 1]);
        H(qubits[n - 1]);
        for i in 0..n - 1 {
            if (not markedState[n - 1 - i]) {
                X(qubits[i]);
            }
        }
    }

    operation GroverDiffusion(qubits : Qubit[]) : Unit is Adj {
       let n = Length(qubits);
        ApplyToEachA(H, qubits);
        ApplyToEachA(X, qubits);
        H(qubits[n - 1]);
        Controlled X(Most(qubits), qubits[n - 1]);
        H(qubits[n - 1]);
        ApplyToEachA(X, qubits);
        ApplyToEachA(H, qubits);            
    } 

    operation grover_algorithm(n : Int, markedState : Bool[], iterations : Int) : Result[] {
        use qubits = Qubit[n];
        let n = Length(qubits);
        ApplyToEachA(H, qubits);
        for _ in 1..iterations {
            GroverOracle(qubits, markedState);
            GroverDiffusion(qubits);
        }
        let results = MeasureEachZ(qubits[0..n - 1]);
        ResetAll(qubits);        
        return results;
    }

    operation RunGrover(n : Int, markedState : Bool[], shots : Int) : Unit {
        mutable resultsCount : (Result[], Int)[] = [];
        //Message($"Resolviendo Simon con {shots} ejecuciones...");
        let iterations = Round(PI() / 4.0 * Sqrt(IntAsDouble(2 ^ n)));
        //Message($"Conteo de resultados: {iterations}");
        // for _ in 1 .. shots {
        let results=grover_algorithm(n, markedState, iterations);
            //mutable found = false;
            //for i in 0..Length(resultsCount) - 1 {
            //    let (existingString, existingCount) = resultsCount[i];
            //    if (existingString == results) {
            //        mutable newResultsCount = resultsCount;
            //        set newResultsCount w/= i <- (results, existingCount + 1);
            //        set resultsCount = newResultsCount;
            //        set found = true;                    
            //    }
            //}
            //if (not found) {
            //    set resultsCount += [(results, 1)];
            //}
        //}
        //Message($"Conteo de resultados: {resultsCount}");
    }
    @EntryPoint()
    operation Main() : Unit {
        RunGrover(3, [true, false, true], 1);      
    }
}