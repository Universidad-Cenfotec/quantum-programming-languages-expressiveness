# Quantum Programming Languages Expressiveness

This repository aims to compare the expressiveness of different quantum programming languages—both hosted (based on existing classical languages) and standalone—by implementing quantum algorithms. The goal is to analyze their capabilities, strengths, and limitations.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Setup and Installation](#setup-and-installation)
   - [Hosted Programming Languages](#hosted-programming-languages)
     - [Qiskit](#qiskit)
     - [Cirq](#cirq)
   - [Standalone Programming Languages](#standalone-programming-languages)
     - [Q#](#q-sharp)
     - [Quipper](#quipper)
     - [Silq](#silq)
3. [Running the Project in Docker](#running-the-project-in-docker)
4. [Contributions](#contributions)
5. [License](#license)

---

## Project Overview

The quantum programming landscape is rapidly evolving. This project compares a range of hosted and standalone quantum programming languages to provide insights into their expressiveness and utility for implementing quantum algorithms.

### Hosted Programming Languages:
- **Qiskit** (Python-based)
- **Cirq** (Python-based)
- **QAPL** (Quantum Algorithm Programming Language)
- **QRISP**

### Standalone Programming Languages:
- **Q#** (Microsoft's quantum programming language)
- **Quipper**
- **Silq**

---

## Setup and Installation

### Hosted Programming Languages

#### **Qiskit**
1. **Install Python**: Ensure Python 3.12.8 is installed.
2. **Windows Setup**:
   - Open a terminal in the project folder.
   - Create a virtual environment:
     ```bash
     python -m venv .venv
     ```
   - Activate the virtual environment:
     ```bash
     .venv\Scripts\activate
     ```
   - Install the required dependencies:
     ```bash
     pip install -r hosted/qiskit/requirements.txt
     ```

3. **Mac/Linux Setup**:
   - Navigate to the project directory.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install the required dependencies:
     ```bash
     pip install -r hosted/qiskit/requirements.txt
     ```

#### **Cirq**
Repeat the steps above using the `hosted/cirq/requirements.txt` file for dependencies.

---

### Standalone Programming Languages
Instructions for setting up the following languages will be added:
- **Q#**
- **Quipper**
- **Silq**

---

## Running the Project in Docker

1. Ensure Docker is installed on your system.
2. Navigate to the folder where the `docker-compose.yml` file is located.
3. Build the Docker container:
   ```bash
   docker compose build
