namespace SimonAlgorithm {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Arrays;

    // Oráculo de Simon
    operation SimonOracle(s : Bool[], qubits : Qubit[]) : Unit {
        let n = Length(s);

        for i in 0..n - 1 {
            if (s[n - 1 - i]) {
                Controlled X([qubits[i]], qubits[n + i]);
            }
        }
    }

    // Algoritmo de Simon
    operation SimonAlgorithm(n : Int, s : Bool[]) : Result[] {
        use qubits = Qubit[2 * n];

        // Aplicamos las puertas Hadamard a los primeros n qubits
        ApplyToEachA(H, qubits[0..n - 1]);

        // Aplicamos el oráculo
        SimonOracle(s, qubits);

        // Aplicamos nuevamente las puertas Hadamard a los primeros n qubits
        ApplyToEachA(H, qubits[0..n - 1]);

        // Medimos los primeros n qubits
        let results = MeasureEachZ(qubits[0..n - 1]);
        ResetAll(qubits);
        
        return results;
    }
    

    // Solver para Simon
    operation SimonSolver(n : Int, s : Bool[], shots : Int) : Unit {
        mutable resultsCount : (Result[], Int)[] = [];
        Message($"Resolviendo Simon con {shots} ejecuciones...");
        
        for _ in 1 .. shots {
            let results = SimonAlgorithm(n, s);
           // let resultString = StringFromResultArray(results);

            mutable found = false;
            for i in 0..Length(resultsCount) - 1 {
                let (existingString, existingCount) = resultsCount[i]; // Destructuring
                if (existingString == results) {
                    mutable newResultsCount = resultsCount;
                    set newResultsCount w/= i <- (results, existingCount + 1);
                    set resultsCount = newResultsCount;
                    set found = true;
                    
                }
            }
            if (not found) {
                set resultsCount += [(results, 1)];
            }
        }

        // Mostrar el conteo de los resultados
        Message($"Conteo de resultados: {resultsCount}");
    }

    @EntryPoint()
    operation Main() : Unit {
        let n = 3;
        let s = [true, false, true]; // Representación del string "101" en binario
        let shots = 100; // Número de ejecuciones
        SimonSolver(n, s,shots);
    }
}