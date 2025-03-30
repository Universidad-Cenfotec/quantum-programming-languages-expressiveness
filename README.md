# Quantum Programming Languages Expressiveness

![Quantum Computing](https://img.shields.io/badge/Quantum-Computing-blue.svg) ![Metrics](https://img.shields.io/badge/Metrics-LOC%20%7C%20CC%20%7C%20Halstead-orange.svg) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-Apache%202.0-blue)


This repository evaluates the expressiveness of various quantum programming languages, both hosted (based on existing classical languages) and standalone. By implementing well-known quantum algorithms, we aim to analyze their strengths, limitations, and overall utility through metrics such as Cyclomatic Complexity (McCabe), Lines of Code (LOC), and Halstead Complexity. This approach provides insights into how effectively these languages enable the construction of correct and efficient quantum algorithms.

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
- Can metrics like McCabe’s Cyclomatic Complexity, Lines of Code (LOC)  and Halstead metrics provide meaningful insights into the utility and efficiency of these languages?

By comparing five hosted quantum programming languages and two standalone quantum languages, this repository sheds light on their expressiveness and productivity.

---

## 🚀 Quantum Programming Languages

### 🏗️ Hosted Languages

These languages are extensions or embedded Domain-Specific Languaages (eDSL) built on top of classical programming languages, allowing developers to leverage existing ecosystems and tools:

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

Three core metrics are used to evaluate the expressiveness of quantum programming languages:

1. **🧩 Cyclomatic Complexity (McCabe’s Complexity):**  
   This metric measures the complexity of a program’s control flow, quantifying the number of linearly independent paths in the code.

2. **📏 Lines of Code (LOC):**  
   LOC provides a simple count of the number of lines of source code, excluding comments and empty lines. A lower LOC for the same algorithm suggests higher expressiveness.

3. **🧠 Halstead Metrics – Lexical Complexity:**
Developed by Maurice Halstead, these metrics measure the lexical complexity of a program based on its operators and operands. From these values, Halstead defines several derived metrics:


   - **Program Vocabulary:** The total number of unique symbols (operators and operands): n = n1 + n2

   - **Program Length:** The total number of lexical tokens: N = N1 + N2

   - **Volume (V):** Represents the size of the implementation in terms of information content: V = N · log2 (n). A higher volume indicates more information is encoded in the program, which may imply greater effort to comprehend or maintain it.

   - **Difficulty (D):** Estimates the cognitive difficulty of understanding or writing the program:
D = n1 / 2 · N2 / n2. This metric increases with more complex or less reusable code elements.

   - **Effort (E):** Measures the total mental effort required to develop or understand the code: E = D · V. Effort correlates with development time and is often used as an indicator of programming complexity.



---

## 📚 Analyzed Quantum Algorithms

To evaluate expressiveness, we implement and analyze the following quantum algorithms:

- **🔎 Deutsch-Jozsa Algorithm**
- **🔍 Simon’s Algorithm**
- **📡 Bernstein-Vazirani Algorithm**
- **🔑 Grover’s Search Algorithm**

These algorithms serve as benchmarks to compare how different quantum languages handle quantum computation primitives and abstractions.

---

## ⚙️ Setup and Installations
1. **Clone the repository** 
To begin, clone the repository to your local machine using the following command:
```bash
git clone https://github.com/Universidad-Cenfotec/quantum-programming-languages-expressiveness.git
```
This will create a local copy of the project on your machine. After cloning, navigate to the project directory:
```
cd https://github.com/Universidad-Cenfotec/quantum-programming-languages-expressiveness.git
```

2. **Installation Options** 
There are two ways to set up the environment for this project: using a virtual environment or using Docker. Choose one of the following methods:


### 🖥️ Local Environment
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
###  📦 Docker Environment
Docker allows you to run the project in a containerized environment, ensuring consistency across different machines.

**1. Install Docker:**
Ensure that Docker and Docker Compose are installed on your machine. If you don't have Docker, you can download and install it from here. [Docker](https://www.docker.com/products/docker-desktop/)

**2. Build and run the Docker container:**

After ensuring Docker is installed, navigate to the project directory (if you're not already there) and run the following commands:

   ```
   docker compose build
   docker compose up -d
   ```
This will build the Docker image and start the container in detached mode (-d).

## 📊 Running the Metrics
To generate the metrics (McCabe CC, LOC and Halstead), navigate to the evaluation directory and run the following command on your terminal:
```
cd evaluation
python main.py
```

This will produce CSV files with the calculated metrics, ready for analysis. Then you can go to:
```
evaluation/metrics_analysis.ipynb
```
And run these to generate some informative graphics.

## 🤝 Contributions
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request. Ensure your code adheres to the existing style and includes appropriate tests.


## 📜 License
This project is licensed under the Apache License 2.0. You may freely use, modify, and distribute this software under the terms of the Apache 2.0 License. See the ./LICENSE file for full details.


