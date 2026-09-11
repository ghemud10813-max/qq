"""
dashboard/components/security_panel.py
======================================
Live signature generation and verification.
"""
import streamlit as st
import pandas as pd

from qds.signature import generate_signature
from qds.verification import verify_signature
from security.detector import ThreatDetector
import uuid

def render_verification_panel():
    """Render the live signature verification UI."""
    st.subheader("Live Verification Control")
    st.write("Generate valid QDS signatures and verify them against the physical measurement apparatus.")
    
    col_opt, col_res = st.columns([0.3, 0.7])
    
    with col_opt:
        st.markdown("**Signature Parameters**")
        sig_len = st.number_input("Signature Length (Qubits)", min_value=4, max_value=256, value=16, step=4, key="ver_sig_len")
        t_thresh = st.slider("Acceptance Threshold", min_value=0.0, max_value=1.0, value=0.7, step=0.05)
        seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=42, key="ver_seed")
        
        c1, c2 = st.columns(2)
        run_legit = c1.button("Run Legitimate", type="primary")
        run_test = c2.button("Run Test")
        
        reset = st.button("Reset State")
        
    with col_res:
        if reset:
            st.session_state.ver_result = None
            st.session_state.ver_sig = None
            
        if run_legit or run_test:
            with st.spinner("Preparing states and performing sequential verification..."):
                sig = generate_signature("dashboard_test", length=sig_len, seed=seed)
                # If run_test, we can optionally mess with the signature? User didn't specify.
                # Just verifying it.
                res = verify_signature(sig, threshold=t_thresh)
                
                det = ThreatDetector()
                det_res = det.detect(res, session_id=sig.signature_id)
                
                st.session_state.ver_sig = sig
                st.session_state.ver_result = (res, det_res)
                
                from dashboard.components.metrics import log_event
                log_event(
                    event_type="Legitimate Verification" if run_legit else "Test Verification",
                    action="verify_signature",
                    score=det_res.anomaly_score,
                    decision=det_res.classification
                )
                
        if st.session_state.get("ver_result"):
            res, det_res = st.session_state.ver_result
            sig = st.session_state.ver_sig
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Verification Score", f"{res.verification_score:.4f}")
            c2.metric("Anomaly Score", f"{det_res.anomaly_score:.4f}")
            c3.metric("Match Count", f"{res.matches}/{sig_len}")
            
            status = "ACCEPTED" if res.accepted else "REJECTED"
            color = "green" if res.accepted else "red"
            c4.markdown(f"**Outcome**<br><span style='color:{color}; font-size:1.5em; font-weight:bold;'>{status}</span>", unsafe_allow_html=True)
            
            with st.expander("Signature Structure & Measurements", expanded=True):
                # Build a table of the state choices
                el_data = []
                for el in sig.elements:
                    el_data.append({
                        "Position": el.position,
                        "Eigenstate": el.eigenstate.label,
                        "Basis": el.eigenstate.basis.upper(),
                        "Expected Result": "+1" if el.eigenstate.eigenvalue == 1 else "-1"
                    })
                df = pd.DataFrame(el_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Set parameters and click a run button.")
