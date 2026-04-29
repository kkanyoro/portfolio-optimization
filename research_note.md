# Hybrid Quantum-Classical Portfolio Optimization via QAOA
**Project-Q 24 hours Challenge**

* **Author:** Kevin Kanyoro
* **Institution:** PROJECT-Q × Zuntenium
* **Date:** April 29, 2026

---

## Abstract
This research note details the development and benchmarking of a hybrid quantum-classical optimizer for the Markowitz Mean-Variance Portfolio problem. Utilizing the Quantum Approximate Optimization Algorithm (QAOA), the project translates a multi-objective financial problem into an Ising Hamiltonian. We compare the performance of a classical brute-force approach against a quantum simulated loop, evaluating solution quality, constraint rigor, and computational scalability. Results indicate 100% parity in solution identification at small scales, while highlighting critical hardware-bound limitations regarding inequality constraints and circuit depth.

---

## 1. Introduction
Portfolio optimization is a foundational problem in modern finance, aimed at selecting the optimal distribution of assets to maximize expected return for a given level of risk. As the number of available assets $N$ grows, the combinatorial search space expands at $2^N$, rendering exhaustive classical search intractable for institutional-grade portfolios. This study implements a Quantum/Hybrid approach to explore the feasibility of Quadratic Unconstrained Binary Optimization (QUBO) in solving these landscapes.

## 2. Mathematical Formulation
The optimization is modeled using the Markowitz Mean-Variance framework. We represent the decision as a binary vector $x \in \{0, 1\}^N$, where $x_i = 1$ implies asset inclusion.

**Objective Function:**

$$\min_{x} \left( q \cdot x^T \Sigma x - (1 - q) \cdot \mu^T x \right)$$

**Where:**
* **$\Sigma$:** The covariance matrix representing portfolio risk.
* **$\mu$:** The expected return vector, adjusted for transaction costs.
* **$q$:** The risk-appetite scaling factor, set to 0.5 for neutral weighting.

## 3. Constraint Modeling Approach
To ensure physical and financial validity, three rigorous constraints were mapped into the Hamiltonian using quadratic penalty terms. To optimize for NISQ-era simulators and minimize circuit depth, equality constraints were prioritized over inequalities to eliminate the need for ancillary slack qubits.

* **Constraint 1 (Cardinality):** Exactly $K = 3$ assets must be selected.
* **Constraint 2 (L1 Sector Diversification):** Exactly 2 assets must be chosen from the Layer 1 Network sector (Assets 0, 1, 2).
* **Constraint 3 (DeFi Sector Diversification):** Exactly 1 asset must be chosen from the DeFi Protocol sector (Assets 3, 4, 5).

> **Note:** Inequality constraints like $Budget \leq B$ were intentionally avoided in the final Hamiltonian. Simulation testing revealed that encoding inequalities requires a log-scale addition of slack variables, which expanded the 6-qubit system into a 15-qubit matrix, increasing computational overhead beyond local simulation capabilities.

## 4. Comparative Methodology

### 4.1 Classical Baseline
A brute-force exhaustive search was implemented to evaluate all 64 possible bitstrings. This control group identifies the absolute mathematical global minimum, providing a benchmark for the Sharpe Ratio and execution time.

### 4.2 Quantum/Hybrid (QAOA)
The problem was mapped to a $p=1$ QAOA circuit using Qiskit’s `MinimumEigenOptimizer`. A classical `COBYLA` optimizer was used to tune the gate angles ($\beta, \gamma$) over 100 iterations, simulating a hybrid quantum-classical feedback loop.

## 5. Experimental Results

| Metric                   | Classical Brute Force | QAOA Hybrid (Simulator)  |
| :----------------------- | :-------------------- | :----------------------- |
| **Optimal Bitstring**    | `[1 0 1 0 1 0]`       | `[1 0 1 0 1 0]`          |
| **Expected Return**      | 0.8909                | 0.8909                   |
| **Sharpe Ratio**         | 1.9814                | 1.9814                   |
| **Execution Time**       | 0.0031 seconds        | 10.6494 seconds          |
| **Constraint Adherence** | 100% (Logic-based)    | 100% (Penalty-converged) |

## 6. Critical Evaluation: Quantum Advantage
This prototype does not demonstrate Quantum Advantage. At small scales ($N = 6$), classical brute force is roughly 3,400 times faster than the quantum simulation. The advantage remains theoretical for two primary reasons:

1.  **Simulation Bottleneck:** Simulating quantum statevectors on classical hardware involves exponential matrix multiplication that negates any algorithmic speedup.
2.  **Connectivity Limitations:** High-density covariance matrices require all-to-all qubit connectivity. On real hardware, this necessitates extensive gate overhead, introducing noise that often prevents convergence.

However, the scalability trend is undeniable. While the classical approach faces an exponential barrier at $N > 100$, the QAOA framework maintains polynomial gate scaling, marking it as a critical candidate for future fault-tolerant quantum systems.

## 7. Conclusion
The project successfully achieved mathematical parity between classical and quantum solvers. The implementation demonstrated that categorical sector constraints can be efficiently modeled in a Hamiltonian without circuit bloat.

---

## Resources and Related Research Work

### 1. Academic Foundations (Financial & Quantum)
* Markowitz, H. (1952). **"Portfolio Selection"**: Established Mean-Variance Optimization.
* Farhi, E., Goldstone, J., & Gutmann, S. (2014). **"A Quantum Approximate Optimization Algorithm (QAOA)"**: Introduces the QAOA algorithm and Ising Hamiltonian mapping.
* Barkoutsos, P. K., et al. (2020). **"Improving Variational Quantum Optimization using CVaR"**: Application of VQE and QAOA to financial optimization and constraint handling.

### 2. Technical Documentation & Frameworks
* [Qiskit Optimization Module Documentation](https://docs.quantum.ibm.com/api/qiskit): Formulation of `QuadraticProgram` and `MinimumEigenOptimizer`.
* [Qiskit Primitives (V2) Migration Guide](https://docs.quantum.ibm.com/run/primitives): Implementing `StatevectorSampler` for the 2026 ecosystem.
* [Scipy Optimize (COBYLA) Reference](https://docs.scipy.org/doc/scipy/reference/optimize.html): Classical derivative-free optimizer documentation.

### 3. Industry Reports & Tutorials
* **IBM Quantum Learning**: "Optimization for Financial Services": Mapping financial constraints into QUBO matrices.
* **Quantum Advantage in Finance: Realistic Expectations**: A review of NISQ-era limitations regarding circuit depth and connectivity.
* **Niche Cents (2026)**: ["Quantum Computing: Revolutionizing Finance Risk & Portfolio Strategy"](https://youtu.be/jVG1oZRL3lo): Overview of quantum solutions for "Black Swan" events and complex portfolio combinations.