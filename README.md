# Quantum Programming Languages Expressiveness

![Quantum Computing](https://img.shields.io/badge/Quantum-Computing-blue.svg) ![Metrics](https://img.shields.io/badge/Metrics-LOC%20%7C%20CC-orange.svg) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-MIT-green)

This repository evaluates the expressiveness of various quantum programming languages, both hosted (based on existing classical languages) and standalone. By implementing well-known quantum algorithms, we aim to analyze their strengths, limitations, and overall utility through metrics such as Cyclomatic Complexity (McCabe) and Lines of Code (LOC). This approach provides insights into how effectively these languages enable the construction of correct and efficient quantum algorithms.

---

## 📖 Table of Contents
1. [🔍 Project Overview](#project-overview)
2. [🚀 Quantum Programming Languages](#quantum-programming-languages)
   - [Hosted Languages](#hosted-languages)
   - [Standalone Languages](#standalone-languages)
3. [📏 Expressiveness Metrics](#expressiveness-metrics)
4. [📚 Analyzed Quantum Algorithms](#analyzed-quantum-algorithms)
5. [⚙️ Setup and Installation](#setup-and-installation)
   - [🖥️ Local Environment](#local-environment)
   - [📦 Docker Environment](#docker-environment)
6. [📊 Running the Metrics](#running-the-metrics)
7. [🤝 Contributions](#contributions)
8. [📜 License](#license)

---

## 🔍 Project Overview

Programming languages form the foundation for software development. They define syntax, semantics, and paradigms that directly impact how algorithms are conceptualized and implemented. While classical languages have matured over time, quantum programming introduces unique challenges that require new abstractions and frameworks. Quantum languages must handle phenomena such as superposition, entanglement, and interference—concepts that have no direct analogs in classical programming.

This project explores the following questions:
- How does the expressiveness of quantum programming languages compare across hosted and standalone paradigms?
- What makes a quantum language "expressive," and how do we quantify that expressiveness?
- Can metrics like McCabe’s Cyclomatic Complexity and Lines of Code (LOC) provide meaningful insights into the utility and efficiency of these languages?

By comparing five hosted quantum programming languages and two standalone quantum languages, this repository sheds light on their expressiveness and productivity.

---

## 🚀 Quantum Programming Languages

### 🏗️ Hosted Languages

These languages are extensions or libraries built on top of classical programming languages, allowing developers to leverage existing ecosystems and tools:

- **[Qiskit](https://qiskit.org/)** (Python-based)
- **[Cirq](https://quantumai.google/cirq)** (Python-based)
- **[quAPL](https://github.com/nunezco2/quAPL)** (Quantum Array Programming Language)
- **[Qrisp](https://qrisp.eu/index.html)** (Python-based)

### 🏆 Standalone Languages

These languages were created specifically for quantum programming, offering unique syntax and constructs to handle quantum concepts directly:

- **[Q#](https://learn.microsoft.com/en-us/azure/quantum/)** (Microsoft’s quantum programming language)
- **[Qmod](https://docs.classiq.io/latest/qmod-reference/language-reference/)** (Classiq’s quantum programming language)

---

## 📏 Expressiveness Metrics

Two core metrics are used to evaluate the expressiveness of quantum programming languages:

1. **🧩 Cyclomatic Complexity (McCabe’s Complexity):**  
   This metric measures the complexity of a program’s control flow, quantifying the number of linearly independent paths in the code.

2. **📏 Lines of Code (LOC):**  
   LOC provides a simple count of the number of lines of source code, excluding comments and empty lines. A lower LOC for the same algorithm suggests higher expressiveness.

Additionally, we incorporate:
- **🔄 Observational Equivalence:** Measures whether two programs exhibit identical behavior in all execution contexts.
- **📉 Kolmogorov Complexity:** Defines the shortest binary program capable of producing a given output, offering insights into syntactic expressiveness.

---

## 📚 Analyzed Quantum Algorithms

To evaluate expressiveness, we implement and analyze the following quantum algorithms:

- **🔎 Deutsch-Jozsa Algorithm**
- **🔍 Simon’s Algorithm**
- **📡 Bernstein-Vazirani Algorithm**
- **🔑 Grover’s Search Algorithm**

These algorithms serve as benchmarks to compare how different quantum languages handle quantum computation primitives and abstractions.

---

## ⚙️ Setup and Installation

### 🖥️ Local Environment

1. **Install Python:** Ensure Python 3.12.8 (or later) is installed.
2. **Windows Setup:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
###  📦 Docker Environment
Ensure Docker and Docker Compose are installed.
Build and run the Docker container:

   ```
   docker compose build
   docker compose up -d
   ```


## 📊 Running the Metrics
To generate the metrics (McCabe and LOC), navigate to the evaluation directory and run:
```
cd evaluation
python main.py
```

This will produce CSV files with the calculated metrics, ready for analysis.


## 🤝 Contributions
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure your code adheres to the existing style and includes appropriate tests.


## 📜 License
This project is licensed under the _______ License.

