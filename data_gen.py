import numpy as np
import pandas as pd

def generate_financial_data(n_assets=6, seed=35):
    # Set seed
    np.random.seed(seed)
    
    asset_names = [f"Asset_{i+1}" for i in range(n_assets)]
    
    # Simulate 1 year of daily returns
    daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=(252, n_assets))
    df_returns = pd.DataFrame(daily_returns, columns=asset_names)
    
    # mu
    expected_returns = df_returns.mean() * 252
    
    # sigma
    cov_matrix = df_returns.cov() * 252
    
    # Transaction cost constraint
    transaction_costs = np.random.uniform(low=0.005, high=0.020, size=n_assets)
    transaction_costs = pd.Series(transaction_costs, index=asset_names)
    
    adjusted_returns = expected_returns - transaction_costs

    return expected_returns, cov_matrix, transaction_costs, adjusted_returns

# Execution
if __name__ == "__main__":
    mu, sigma, t_costs, mu_adjusted = generate_financial_data(n_assets=6)
    
    print("1. Original Expected Returns (\u03bc)")
    print(mu.round(4))
    print("\n2. Transaction Costs")
    print(t_costs.round(4))
    print("\n3. Adjusted Returns (\u03bc_adjusted)")
    print(mu_adjusted.round(4))
    print("\n4. Covariance Matrix (\u03a3)")
    print(sigma.round(4))