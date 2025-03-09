# Quantum Programming Languages Expressiveness

This repository evaluates the expressiveness of various quantum programming languages, both hosted (based on existing classical languages) and standalone. By implementing well-known quantum algorithms, we aim to analyze their strengths, limitations, and overall utility through metrics such as Cyclomatic Complexity (McCabe) and Lines of Code (LOC). This approach provides insights into how effectively these languages enable the construction of correct and efficient quantum algorithms.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Quantum Programming Languages](#quantum-programming-languages)
   - [Hosted Languages](#hosted-languages)
   - [Standalone Languages](#standalone-languages)
3. [Expressiveness Metrics](#expressiveness-metrics)
4. [Setup and Installation](#setup-and-installation)
   - [Local Environment](#local-environment)
   - [Docker Environment](#docker-environment)
5. [Running the Metrics](#running-the-metrics)
6. [Contributions](#contributions)
7. [License](#license)

---

## Project Overview

Programming languages form the foundation for software development. They define syntax, semantics, and paradigms that directly impact how algorithms are conceptualized and implemented. While classical languages have matured over time, quantum programming introduces unique challenges that require new abstractions and frameworks. Quantum languages must handle phenomena such as superposition, entanglement, and interference—concepts that have no direct analogs in classical programming.

This project explores the following questions:
- How does the expressiveness of quantum programming languages compare across hosted and standalone paradigms?
- What makes a quantum language "expressive," and how do we quantify that expressiveness?
- Can metrics like McCabe’s Cyclomatic Complexity and Lines of Code (LOC) provide meaningful insights into the utility and efficiency of these languages?

By comparing five hosted quantum programming languages and two standalone quantum languages, this repository sheds light on their expressiveness and productivity.

---

## Quantum Programming Languages

### Hosted Languages

These languages are extensions or libraries built on top of classical programming languages, allowing developers to leverage existing ecosystems and tools:

- **[Qiskit](https://qiskit.org/)** (Python-based): Provides a comprehensive toolkit for building and running quantum circuits on simulators and real quantum hardware.
- **[Cirq](https://quantumai.google/cirq)** (Python-based): Focuses on building, simulating, and running quantum circuits, especially on near-term quantum hardware.
- **[quAPL](https://github.com/nunezco2/quAPL)** (Quantum Array Programming Language): Designed to work seamlessly with quantum array operations, inspired by APL.
- **[Qrisp](https://qrisp.eu/index.html)** (Python-based): A lightweight framework for exploring quantum algorithms.

### Standalone Languages

These languages were created specifically for quantum programming, offering unique syntax and constructs to handle quantum concepts directly:

- **[Q#](https://learn.microsoft.com/en-us/azure/quantum/)** (Microsoft’s quantum programming language): Provides high-level abstractions, type safety, and integration with classical code to write robust quantum algorithms.
- **[Qmod](https://docs.classiq.io/latest/qmod-reference/language-reference/)** (Classiq’s quantum programming language): Focused on modeling and synthesizing quantum circuits.

---

## Expressiveness Metrics

Two core metrics are used to evaluate the expressiveness of quantum programming languages:

1. **Cyclomatic Complexity (McCabe’s Complexity):**  
   This metric measures the complexity of a program’s control flow. It helps quantify how many linearly independent paths exist through a program. A higher cyclomatic complexity generally indicates more complex logic, which may be harder to understand and maintain.

2. **Lines of Code (LOC):**  
   LOC provides a simple count of the number of lines of source code, excluding comments and empty lines. While it doesn’t directly measure complexity, LOC can highlight how concisely a language allows algorithms to be expressed.

By combining these metrics, the project compares the hosted and standalone quantum languages in terms of their ability to succinctly and clearly express quantum algorithms.

---

## Setup and Installation

### Local Environment

1. **Install Python:**  
   Make sure Python 3.12.8 (or later) is installed on your system.

2. **Windows Setup:**  
   - Navigate to the project directory.  
   - Create a virtual environment:  
     ```bash
     python -m venv .venv
     ```
   - Activate the virtual environment:  
     ```bash
     .venv\Scripts\activate
     ```
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

3. **Mac/Linux Setup:**  
   - Navigate to the project directory.  
   - Create and activate a virtual environment:  
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

### Docker Environment

1. **Ensure Docker and Docker Compose are installed:**  
   - [Docker](https://www.docker.com/products/docker-desktop)  
   - [Docker Compose](https://docs.docker.com/compose/)

2. **Build and run the Docker container:**  
   - Open a terminal in the project folder.  
   - Build the Docker image:  
     ```bash
     docker compose build
     ```
   - Start the container:  
     ```bash
     docker compose up -d
     ```

---

## Running the Metrics

To generate the metrics (McCabe and LOC), navigate to the `evaluation` directory and run:

```bash
cd evaluation
python main.py
```

This will produce CSV files with the calculated metrics, ready for analysis.

## Contributions
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Before contributing, ensure that your code adheres to the existing style and includes appropriate tests.

## License


