import streamlit as st
import numpy as np
import pandas as pd

# Import your existing logic
from data_gen import generate_financial_data
from classical_solver import classical_brute_force
from quantum_solver import build_quantum_model, solve_with_qaoa

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Quantum Portfolio Optimizer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SIDEBAR CONTROLS
st.sidebar.title("Optimization Engine")
st.sidebar.markdown("Configure the parameters for the Markowitz Mean-Variance framework.")

# Risk Slider
q_param = st.sidebar.slider("Risk Appetite (q)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

st.sidebar.markdown("---")
st.sidebar.markdown("**Constraints Enforced:**")
st.sidebar.markdown("- Cardinality: Exactly 3 Assets")
st.sidebar.markdown("- Sector 1 (L1): Exactly 2 Assets")
st.sidebar.markdown("- Sector 2 (DeFi): Exactly 1 Asset")

st.sidebar.markdown("---")
run_button = st.sidebar.button("Execute Hybrid Pipeline", type="primary", use_container_width=True)

# MAIN DASHBOARD
st.title("The Quantum Edge: Portfolio Optimization")
st.markdown("Project-Q × Zuntenium 24-Hour Challenge Prototype")

# Data Generation (Constant seed for stable presentation)
_, sigma, _, mu_adjusted = generate_financial_data(n_assets=6, seed=35)
prices = np.array([5, 2, 8, 4, 6, 3]) 

# Wait for user execution
if not run_button:
    st.info("Configure risk parameters and click 'Execute Hybrid Pipeline' to begin.")
    
    # Show the baseline data
    st.subheader("Asset Universe (N=6)")
    asset_data = pd.DataFrame({
        "Asset Sector": ["Layer 1", "Layer 1", "Layer 1", "DeFi", "DeFi", "DeFi"],
        "Expected Return (%)": np.round(mu_adjusted * 100, 2),
        "Price ($)": prices
    })
    st.dataframe(asset_data, use_container_width=True)

else:
    # --- EXECUTION PHASE ---
    col1, col2 = st.columns(2)
    
    # 1. Classical Execution
    with col1:
        st.subheader("Classical Brute Force")
        with st.spinner("Evaluating all 64 combinations..."):
            best_x_class, metrics_class, ex_time_class = classical_brute_force(
                mu_adjusted, sigma, k_assets=3, q=q_param
            )
            
        if best_x_class is not None:
            st.success(f"Converged in {ex_time_class:.4f} seconds")
            st.metric("Optimal Bitstring", str(best_x_class))
            
            subcol1, subcol2 = st.columns(2)
            subcol1.metric("Adjusted Return", f"{metrics_class['return'] * 100:.2f}%")
            subcol2.metric("Sharpe Ratio", f"{metrics_class['sharpe']:.4f}")
        else:
            st.error("No valid classical portfolio found.")

    # 2. Quantum Execution
    with col2:
        st.subheader("QAOA Hybrid Simulator")
        with st.spinner("Tuning quantum circuit via COBYLA..."):
            portfolio_problem = build_quantum_model(
                mu_adjusted, sigma, k_assets=3, q=q_param
            )
            qaoa_result, ex_time_quant = solve_with_qaoa(portfolio_problem)
            
            # Extract bits
            best_x_quant = np.array(qaoa_result.x[:6])
            
        st.success(f"Converged in {ex_time_quant:.4f} seconds")
        st.metric("Optimal Bitstring", str(best_x_quant))
        
        # Verify Constraints
        st.markdown("**Constraint Verification:**")
        l1_count = sum(best_x_quant[0:3])
        defi_count = sum(best_x_quant[3:6])
        
        st.checkbox(f"Cardinality (3) — Found: {sum(best_x_quant)}", value=(sum(best_x_quant) == 3), disabled=True)
        st.checkbox(f"Layer 1 Target (2) — Found: {l1_count}", value=(l1_count == 2), disabled=True)
        st.checkbox(f"DeFi Target (1) — Found: {defi_count}", value=(defi_count == 1), disabled=True)

    # 3. Scalability Alert
    st.markdown("---")
    if np.array_equal(best_x_class, best_x_quant):
        st.info(f"**Parity Achieved:** The quantum simulator successfully collapsed into the classical global minimum.")