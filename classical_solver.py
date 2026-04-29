import numpy as np
import itertools
import time
from data_gen import generate_financial_data

def calculate_objective(x, mu, sigma, q=0.5, risk_free_rate=0.02):
    """
    Calculates the multi-objective score, return, risk, and Sharpe Ratio.
    """
    port_return = np.dot(x, mu)
    port_risk = np.dot(x, np.dot(sigma, x))
    score = (q * port_risk) - ((1 - q) * port_return)
    
    # Sharpe Ratio - sqrt of port_risk(variance) to get standard deviation
    if port_risk > 0:
        sharpe_ratio = (port_return - risk_free_rate) / np.sqrt(port_risk)
    else:
        sharpe_ratio = 0
        
    return score, port_return, port_risk, sharpe_ratio

def classical_brute_force(mu, sigma, k_assets, q=0.5):
    """
    Checks all combinations, enforces constraints, and logs metrics.
    """
    n_assets = len(mu)
    best_score = float('inf')
    best_portfolio = None
    best_metrics = {}
    
    all_combinations = list(itertools.product([0, 1], repeat=n_assets))
    
    start_time = time.time()
    
    for combo in all_combinations:
        x = np.array(combo)
        
        # Cardinality constraint
        if np.sum(x) != k_assets:
            continue 
            
        score, ret, risk, sharpe = calculate_objective(x, mu, sigma, q)
        
        # Sector diversification constraints
        # Exactly 2 Layer 1s and exactly 1 DeFi
        if np.sum(x[0:3]) != 2 or np.sum(x[3:6]) != 1:
            continue
            
        # save the portfolo with lower score
        if score < best_score:
            best_score = score
            best_portfolio = x
            best_metrics = {
                'return': ret, 
                'risk': risk, 
                'score': score,
                'sharpe': sharpe
            }
            
    end_time = time.time()
    exec_time = end_time - start_time
    
    return best_portfolio, best_metrics, exec_time

if __name__ == "__main__":
    _, sigma, _, mu_adjusted = generate_financial_data(n_assets=6, seed=35)
    
    # constraint parameters
    K_ASSETS = 3
    Q_PARAM = 0.5 
    
    best_x, metrics, ex_time = classical_brute_force(
        mu_adjusted, 
        sigma, 
        k_assets=K_ASSETS, 
        q=Q_PARAM
    )
    
    print("CLASSICAL BRUTE FORCE RESULTS")
    if best_x is not None:
        print(f"Optimal Portfolio (Bitstring): {best_x}")
        print(f"Expected Return (Adjusted):    {metrics['return']:.4f}")
        print(f"Portfolio Risk (Variance):     {metrics['risk']:.4f}")
        print(f"Sharpe Ratio:                  {metrics['sharpe']:.4f}")
        print(f"Master Objective Score:        {metrics['score']:.4f}")
        print(f"Execution Time:                {ex_time:.6f} seconds")
    else:
        print("No valid portfolio found that meets all constraints.")