# Q# Primitive Types

## Numeric Types
- **`Int`** – Represents an integer (e.g., `3`, `-1`, `42`).
- **`BigInt`** – Represents arbitrarily large integers.
- **`Double`** – Represents a floating-point number (e.g., `3.14`, `-2.718`).

## Boolean Type
- **`Bool`** – Represents a boolean value (`true` or `false`).

## Quantum-Specific Types
- **`Qubit`** – Represents a quantum bit (cannot be directly accessed).
- **`Pauli`** – Represents one of the four Pauli operators:  
  - `PauliI`  
  - `PauliX`  
  - `PauliY`  
  - `PauliZ`
- **`Result`** – Represents the outcome of a quantum measurement (`Zero` or `One`).

## Sequence and Text Types
- **`Range`** – Represents a sequence of integers (e.g., `1..5` or `2..2..10`).
- **`String`** – Represents a sequence of characters.

## Special Type
- **`Unit`** – Represents a function return type that does not return a value (similar to `void` in other languages).

## Composite Types
- **Tuples** – A fixed-size collection of values (e.g., `(Int, Double)`).
- **Arrays** – A collection of elements of the same type (e.g., `Int[]`, `Qubit[]`).
- **User-defined types** – Custom data structures that encapsulate values.

---

## Summary Table of Q# Primitive Types

| Type     | Description |
|----------|------------|
| `Int`    | Integer numbers (e.g., `3`, `-1`, `42`). |
| `BigInt` | Arbitrarily large integers. |
| `Double` | Floating-point numbers (e.g., `3.14`, `-2.718`). |
| `Bool`   | Boolean values (`true`, `false`). |
| `Qubit`  | Represents a quantum bit (not directly accessible). |
| `Pauli`  | Represents one of the four Pauli operators (`PauliI`, `PauliX`, `PauliY`, `PauliZ`). |
| `Result` | The outcome of a quantum measurement (`Zero`, `One`). |
| `Range`  | Represents a sequence of integers (e.g., `1..5`, `2..2..10`). |
| `String` | A sequence of characters. |
| `Unit`   | A function return type that does not return a value. |

