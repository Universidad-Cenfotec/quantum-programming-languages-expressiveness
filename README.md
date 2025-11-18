# Is Productivity in Quantum Programming Equivalent to Expressiveness?

![Quantum Computing](https://img.shields.io/badge/Quantum-Computing-blue.svg) ![Metrics](https://img.shields.io/badge/Metrics-LOC%20%7C%20CC%20%7C%20Halstead-orange.svg) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-Apache%202.0-blue)


This repository contains the source code, experimental data, and analysis tools for the research paper **"Is Productivity in Quantum Programming Equ⌈ivalent to Expressiveness?"**.

We present a comparative analysis of **Hosted** and **Standalone** quantum programming languages. By implementing a diverse set of quantum algorithms—ranging from fundamental oracles to the Quantum Fourier Transform (QFT)—we quantitatively evaluate their expressiveness and potential for developer productivity using software engineering metrics.

---

## 📖 Table of Contents
1. [Abstract](#-abstract)
2. [Scope of the Study](#-scope-of-the-study)
   - [Languages Analyzed](#languages-analyzed)
   - [Algorithms Implemented](#algorithms-implemented)
3. [Methodology & Metrics](#-methodology--metrics)
4. [Repository Structure](#-repository-structure)
3. [Setup & Reproducibility](#-setup--reproducibility)
6. [Running the Analysis](#-running-the-analysis)
7. [Contributions](#-contributions)
7. [LICENSE](#-license)

---

## 📄 Abstract

The expressiveness of quantum programming languages plays a crucial role in the efficient and comprehensible representation of quantum algorithms. Unlike classical languages with mature abstraction mechanisms, quantum languages must integrate cognitively challenging concepts such as superposition, interference, and entanglement while maintaining clarity.

This project investigates the landscape of expressiveness through a comparative analysis of **9 quantum programming languages**. We evaluate how these languages support the implementation of core quantum algorithms using **Lines of Code (LOC)**, **Cyclomatic Complexity (CC)**, and **Halstead Complexity (HC)** metrics. Our findings suggest that distinct trade-offs exist between expressiveness (abstraction) and productivity (cognitive load and implementation effort).

---

## 🔭 Scope of the Study

### Languages Analyzed
We categorize the languages into two paradigms, highlighting the evolution of assembly languages and modern high-level frameworks.

#### Hosted Languages (eDSLs)
Extensions or libraries built on top of classical languages (primarily Python and APL):
- **[PennyLane](https://pennylane.ai/)** (Xanadu) - A leading library for differentiable programming of quantum computers.
- **[Qiskit](https://qiskit.org/)** (IBM) - A comprehensive framework for gate-based quantum computing.
- **[Cirq](https://quantumai.google/cirq)** (Google) - Focused on NISQ algorithms and hardware control.
- **[Qrisp](https://qrisp.eu/)** - A high-level framework for structured quantum programming.
- **[quAPL](https://github.com/nunezco2/quAPL)** - An array-based quantum programming language embedded in APL.


#### Standalone & Assembly Languages
Languages designed specifically for the quantum domain, from low-level description to high-level synthesis:
- **[OpenQASM 2.0](https://openqasm.com/)** - The standard intermediate representation for quantum circuits.
- **[OpenQASM 3.0](https://openqasm.com/)** - A significant evolution introducing classical control flow and pulse-level control.
- **[Q#](https://learn.microsoft.com/en-us/azure/quantum/)** (Microsoft) - A high-level, domain-specific language for scalable quantum computing.
- **[Qmod](https://www.classiq.io/)** (Classiq) - A high-level language for quantum logic synthesis.


### Algorithms Implemented

The benchmarks selected cover fundamental primitives, oracle-based speedups, and basis transformations:
1. **Deutsch-Jozsa**
2. **Bernstein-Vazirani**
3. **Simon’s Algorithm**
4. **Grover’s Search**
5. **Quantum Fourier Transform (QFT)** - A key subroutine in many advanced quantum algorithms (e.g., Shor's, QPE).


---

## 📏 Methodology & Metrics

We utilize a custom Python-based analysis engine to parse and evaluate the source code based on:

1. **Syntactic Verbosity:**
   - **Lines of Code (LOC):** Measures conciseness by counting non-empty, non-comment lines.

2. **Control Flow Complexity:**
   - **Cyclomatic Complexity (CC):** Measures the number of linearly independent paths (branching logic) required to define the circuit or algorithm.

3. **Cognitive & Lexical Complexity (Halstead Metrics):**
   - **Volume (V):** Information content based on operators/operands.
   - **Difficulty (D):** Error-proneness and implementation difficulty.
   - **Effort (E):** Mental effort required to write the program ($E = D \times V$).

4. **Derived Ratios:**
   - **Control Flow Density:** $CC / LOC$
   - **Cognitive Load per Line:** $Effort / LOC$

---

## 📂 Repository Structure

```bash
.
├── classic/                 # Classical baseline implementations (Python)
├── evaluation_metrics/      # Core analysis engine (Python)
│   ├── core/                # Scanners and analyzer logic
│   ├── metrics/             # Individual metric implementations (CC, LOC, Halstead)
│   ├── plotting/            # Visualization scripts (Scatter plots, Radar charts)
│   └── results/             # Generated CSVs and Plots
├── hosted/                  # Source code for hosted languages
│   ├── cirq/
│   ├── pennylane/           # PennyLane implementations
│   ├── qiskit/
│   ├── qrisp/
│   └── quapl/
├── standalone/              # Source code for standalone languages
│   ├── q#/
│   ├── qasm/                # OpenQASM 2.0
│   ├── qasm3/               # OpenQASM 3.0
│   └── qmod/
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
└── docker-compose.yml       # Orchestration

```
---

## 🔧 Setup & Reproducibility

### 1. Clone the repository 
To begin, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/Universidad-Cenfotec/quantum-programming-languages-expressiveness.git
```
This will create a local copy of the project on your machine. After cloning, navigate to the project directory:

```
cd https://github.com/Universidad-Cenfotec/quantum-programming-languages-expressiveness.git
```

### 2. Required Extensions
For running Q# and QASM programs, you'll need to install the Azure Quantum Development Kit (QDK) extension for Visual Studio Code:
1. Open VS Code
2. Go to the Extensions view (Ctrl+Shift+X)
3. Search for "Azure Quantum Development Kit (QDK)"
4. Click Install
For more information about the QDK extension, visit the [official QDK repository](https://github.com/microsoft/qdk).

### 3. Installation Options 
There are two ways to set up the environment for this project: using a virtual environment or using Docker. Choose one of the following methods:


#### 3.1 Local Environment
Using a virtual environment ensures that the project dependencies do not interfere with other Python projects on your machine.
1. **Install Python:**
 Ensure Python 3.12.8 (or later) is installed.

2. **Setup:**
In case that you prefer running locally, is recommended to create a virtual environment
- For Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   ```
   pip install -r requirements.txt
   ```
- For Mac/Linux:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
   ```
   pip install -r requirements.txt
   ```
#### 3.2 Docker Environment
Docker allows you to run the project in a containerized environment, ensuring consistency across different machines.

1. **Install Docker:**
Ensure that Docker and Docker Compose are installed on your machine. If you don't have Docker, you can download and install it from here. [Docker](https://www.docker.com/products/docker-desktop/)

2. **Build and run the Docker container:**
After ensuring Docker is installed, navigate to the project directory (if you're not already there) and run the following commands:
   ```
   docker compose build
   docker compose up -d
   ```
   This will build the Docker image and start the container in detached mode (-d).

---

## 📊 Running the Analysis
Our analysis pipeline is automated. You can generate the raw data (CSVs) and the visualizations used in the paper. To generate the metrics (McCabe CC, LOC and Halstead), navigate to the evaluation directory and run the following command on your terminal (Remember to have the virtual environment active):
```
python -m evaluation_metrics.main
```

This will produce CSV files with the calculated metrics, ready for analysis. Then you can go to:
```
python -m evaluation_metrics.menu
```
And run these to generate some informative graphics. 
Output: Plots will be saved in evaluation_metrics/results/graphics/.

---

## 🤝 Contributions
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure your code adheres to the existing style and includes appropriate tests.

---

## 📜 License
This project is licensed under the Apache License 2.0. See the LICENSE file for details.


