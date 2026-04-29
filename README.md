# Hybrid Quantum-Classical Portfolio Optimization via QAOA
### Project-Q 24 hours Challenge

This repository contains a hybrid quantum-classical solver. The project implements the **Quantum Approximate Optimization Algorithm (QAOA)** to solve the Markowitz Mean-Variance Portfolio problem, benchmarking its performance against a classical brute-force baseline.

## Project Overview
The goal is to select an optimal distribution of $N=6$ assets to maximize return while minimizing risk, subject to specific structural constraints. The project translates this multi-objective financial problem into an **Ising Hamiltonian** and solves it using a hybrid feedback loop.

### Key Features
* **Mathematical Framework:** Markowitz Mean-Variance optimization.
* **Quantum Algorithm:** Implementation of QAOA with $p=1$ using Qiskit's `MinimumEigenOptimizer`.
* **Hybrid Loop:** Classical `COBYLA` optimizer with 100 iterations for parameter tuning.
* **Advanced Constraints:** Categorical sector diversification and cardinality enforcement.

## Tech Stack & Installation
The project is built using Python 3.10+ and the following libraries:
* **Qiskit / Qiskit-Optimization:** Quantum circuit construction and optimization wrappers.
* **NumPy / Pandas:** Data manipulation and matrix algebra.
* **Matplotlib:** Financial data visualization.
* **SciPy:** Classical optimization primitives.

### Installation
```bash
# Clone the repository
git clone https://github.com/kkanyoro/portfolio-optimization
cd portfolio-optimization

# Install dependencies
pip install qiskit qiskit-optimization numpy pandas matplotlib scipy
```

## Mathematical Formulation
The optimizer seeks the binary vector $x \in \{0, 1\}^N$ that minimizes the following objective function:

$$\min_{x} \left( q \cdot x^T \Sigma x - (1 - q) \cdot \mu^T x \right)$$

Where:
* **$\Sigma$**: Covariance matrix representing portfolio risk.
* **$\mu$**: Expected return vector, adjusted for transaction costs.
* **$q$**: Risk-appetite scaling factor (set to 0.5).

### Constraints
To ensure validity in a NISQ-era environment, the following equality constraints were encoded as penalty terms in the Hamiltonian:
1.  **Cardinality:** Exactly $K=3$ assets must be selected.
2.  **Sector 1 (Layer 1):** Exactly 2 assets from the Layer 1 Network sector.
3.  **Sector 2 (DeFi):** Exactly 1 asset from the DeFi Protocol sector.

# Experimental Results
The prototype achieved **100% parity** in solution quality between classical and quantum solvers for a 6-asset portfolio.

| Metric                   | Classical Brute Force | QAOA Hybrid (Simulator) |
| :----------------------- | :-------------------- | :---------------------- |
| **Optimal Bitstring**    | `[1 0 1 0 1 0]`       | `[1 0 1 0 1 0]`         |
| **Expected Return**      | 0.8909                | 0.8909                  |
| **Sharpe Ratio**         | 1.9814                | 1.9814                  |
| **Execution Time**       | ~0.0031 seconds       | ~10.6494 seconds        |
| **Constraint Adherence** | 100%                  | 100%                    |

## Repository Structure
* `data_gen.py`: Synthetic financial data generation.
* `classical_solver.py`: Brute-force exhaustive search implementation.
* `quantum_solver.py`: QAOA implementation using Qiskit V2 primitives.
* `research_note.md`: Full technical research paper.