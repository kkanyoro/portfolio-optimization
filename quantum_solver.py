import numpy as np
import time
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.primitives import StatevectorSampler
from data_gen import generate_financial_data

def build_quantum_model(mu, sigma, k_assets, q=0.5):
    """
    Translates the portfolio problem into a Qiskit QuadraticProgram.
    """
    mu = np.array(mu)
    sigma = np.array(sigma)
    
    n_assets = len(mu)
    qp = QuadraticProgram(name="Portfolio_Optimization")
    
    # Define binary variables
    for i in range(n_assets):
        qp.binary_var(name=f"x_{i}")
        
    # Objective function
    linear_terms = {f"x_{i}": -1 * (1 - q) * mu[i] for i in range(n_assets)}
    
    quadratic_terms = {}
    for i in range(n_assets):
        for j in range(n_assets):
            if sigma[i, j] != 0:
                quadratic_terms[(f"x_{i}", f"x_{j}")] = q * sigma[i, j]
                
    qp.minimize(linear=linear_terms, quadratic=quadratic_terms)
    
    # Cardinality constraint
    cardinality_dict = {f"x_{i}": 1 for i in range(n_assets)}
    qp.linear_constraint(linear=cardinality_dict, sense="==", rhs=k_assets, name="Cardinality")
    
    # Sector constraint 1
    layer1_dict = {"x_0": 1, "x_1": 1, "x_2": 1}
    qp.linear_constraint(linear=layer1_dict, sense="==", rhs=2, name="Layer1_Constraint")
    
    # Sector constraint 2
    defi_dict = {"x_3": 1, "x_4": 1, "x_5": 1}
    qp.linear_constraint(linear=defi_dict, sense="==", rhs=1, name="DeFi_Constraint")
    
    return qp

def solve_with_qaoa(qp):
    """
    Converts to QUBO and runs the QAOA hybrid algorithm.
    """
    # handles slack variables and penalties automatically
    converter = QuadraticProgramToQubo()
    qubo = converter.convert(qp)
    
    optimizer = COBYLA(maxiter=100)
    sampler = StatevectorSampler()
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=1)
    eigen_optimizer = MinimumEigenOptimizer(qaoa)
    
    # Run and time the execution
    start_time = time.time()
    print("Running QAOA Simulator...")
    result = eigen_optimizer.solve(qubo)
    exec_time = time.time() - start_time
    
    return result, exec_time

if __name__ == "__main__":
    # same environment as classical solver
    _, sigma, _, mu_adjusted = generate_financial_data(n_assets=6, seed=35)
    
    K_ASSETS = 3
    Q_PARAM = 0.5
    
    # Build and Solve
    portfolio_problem = build_quantum_model(
        mu_adjusted, sigma, k_assets=K_ASSETS, q=Q_PARAM
    )

    qaoa_result, ex_time = solve_with_qaoa(portfolio_problem)
    
    # only get the first 6 bits ignoring slack variables
    asset_variables = qaoa_result.x[:6] 
    
    print("\nQAOA HYBRID RESULTS")
    print(f"Optimal Portfolio (Bitstring): {asset_variables}")
    
    # Status Checks
    layer1_count = sum(asset_variables[0:3])
    defi_count = sum(asset_variables[3:6])
    print(f"Total Cardinality Observed:   {sum(asset_variables) == K_ASSETS}")
    print(f"Layer 1 Target (2) Observed:  {layer1_count == 2}")
    print(f"DeFi Target (1) Observed:     {defi_count == 1}")
    print(f"Execution Time:               {ex_time:.4f} seconds")