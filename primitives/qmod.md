| Primitive           | Description                                                                                                                                                                                                                                 |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `qfunc`             | Defines a quantum function that operates on quantum variables. Functions marked with `qfunc` can manipulate quantum data and be composed to build complex algorithms. |
| `qbit`              | Represents a quantum bit (qubit), the fundamental unit of quantum information, capable of existing in a superposition of states 0 and 1. |
| `qnum`              | Represents quantum numbers, allowing for the representation of integers or fixed-point real numbers within quantum computations. |
| `allocate`          | Allocates quantum variables (qubits or quantum numbers) for use within quantum functions. |
| `control`           | Applies a specified quantum function conditionally, based on the state of a given quantum variable. |
| `invert`            | Reverses the action of a specified quantum function, effectively applying its inverse operation. |
| `within_apply`      | Defines a block of quantum operations to be applied within a specific context, allowing for structured quantum programming. |
| `bind`              | Associates quantum variables with specific quantum operations or functions, facilitating modularity in quantum program design. |
| `PHASE`             | Applies a phase shift to a qubit, modifying its state by a specified angle. |
| `hadamard_transform`| Applies the Hadamard transformation to a quantum variable, creating a uniform superposition of its possible states. |

### Source
https://docs.classiq.io/latest/qmod-reference/language-reference/functions/