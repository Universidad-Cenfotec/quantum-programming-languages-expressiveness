namespace GroverAlgorithm {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    /// Crea el oráculo de Grover que invierte la fase del estado marcado.
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

    /// Implementa la difusión de Grover para amplificar el estado marcado.
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

    /// Implementa el algoritmo de Grover.
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

    /// Ejecuta el algoritmo de Grover y muestra los resultados.
    operation RunGrover(n : Int, markedState : Bool[], shots : Int) : Unit {
        mutable resultsCount : (Result[], Int)[] = [];
        Message($"Resolviendo Simon con {shots} ejecuciones...");

        let iterations = Round(PI() / 4.0 * Sqrt(IntAsDouble(2 ^ n)));
        Message($"Conteo de resultados: {iterations}");

        for _ in 1 .. shots {
            let results=grover_algorithm(n, markedState, iterations);

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

    /// Punto de entrada principal.
    @EntryPoint()
    operation Main() : Unit {
        let n = 3;
        let markedState = [true, false, true]; // "101" en binario.
        let shots = 1;

        RunGrover(n, markedState, shots);

        
        
    }
}