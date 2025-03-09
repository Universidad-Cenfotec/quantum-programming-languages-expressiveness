
namespace Source {

    operation Random() : Result {
        use q = Qubit();
        H(q);
        let result = M(q);
        Reset(q);
        return result
    }

    operation RandomNBits(N: Int): Result[] {
        mutable results = [];
        for i in 0 .. N - 1 {
            let r = Random();
            results += [r];
        }
        return results
    }
}