"""
dashboard/components/quantum_view.py
====================================
Quantum noise and visualization panel.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

from qds.pauli_states import get_eigenstate
from quantum.noise import NOISE_TYPES, run_noisy_teleportation, ideal_density_matrix

def render_quantum_noise_panel():
    """Render interactive quantum telemetry and noise analysis."""
    st.subheader("Quantum Teleportation & Noise Injection")
    
    col_ctrl, col_viz = st.columns([0.3, 0.7])
    
    with col_ctrl:
        st.markdown("**Channel Configuration**")
        noise_type = st.selectbox("Noise Model", NOISE_TYPES, index=2) # default to depolarizing
        noise_p = st.slider("Noise Strength (p)", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
        state_label = st.selectbox("Transmit Eigenstate", ["|0>", "|1>", "|+>", "|->", "|+i>", "|-i>"], index=2)
        
        run_btn = st.button("Transmit State")
        
    with col_viz:
        if run_btn:
            st.session_state.quantum_run = True
            
        if st.session_state.get("quantum_run"):
            with st.spinner("Simulating open quantum system..."):
                state = get_eigenstate(state_label)
                # run_noisy_teleportation(noise_type, p, theta, phi)
                res = run_noisy_teleportation(noise_type, noise_p, state.theta, state.phi)
                
                st.metric("Teleportation Fidelity", f"{res.fidelity:.4%}")
                if res.fidelity >= 0.80:
                    st.success(f"Transmission Successful. Fidelity meets minimum threshold (>= 80%).")
                else:
                    st.error(f"Transmission Failed. Fidelity dropped below threshold due to channel noise.")
                    
                # Visualize ideal vs noisy density matrix diagonal
                ideal_dm = ideal_density_matrix(res.theta, res.phi)
                ideal_diag = np.diag(ideal_dm).real
                actual_diag = np.diag(res.bob_density_matrix).real
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=['|0⟩', '|1⟩'], y=ideal_diag, name='Ideal State', marker_color='rgba(0, 255, 65, 0.7)'))
                fig.add_trace(go.Bar(x=['|0⟩', '|1⟩'], y=actual_diag, name='Received State', marker_color='rgba(255, 7, 58, 0.7)'))
                fig.update_layout(template="plotly_dark", barmode='group', title="Density Matrix Projection Probabilities", yaxis_range=[0, 1])
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Configure channel parameters and click Transmit State.")
