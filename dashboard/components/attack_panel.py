"""
dashboard/components/attack_panel.py
====================================
Interactive Premium Attack simulation panel with 3D Quantum Networking visual.
"""
import streamlit as st
import time
import pandas as pd

from attacks.runner import AttackRunner
from attacks.forgery import ForgeryAttack
from attacks.impersonation import ImpersonationAttack
from attacks.replay import ReplayAttack
from attacks.unauthorized_verification import UnauthorizedVerificationAttack
from attacks.channel_manipulation import ChannelManipulationAttack

from security.detector import ThreatDetector
from dashboard.components.attack_simulation_3d import render_3d_simulation

ATTACKS = {
    "FORGERY": ForgeryAttack,
    "IMPERSONATION": ImpersonationAttack,
    "REPLAY": ReplayAttack,
    "UNAUTHORIZED_VERIFICATION": UnauthorizedVerificationAttack,
    "CHANNEL_MANIPULATION": ChannelManipulationAttack,
}

def render_attack_panel():
    st.subheader("Interactive Quantum-Cyber Attack Simulation")
    st.write("Visually inject and analyze quantum interception, forgery, or replay threats against QVERIS.")

    if "attack_history" not in st.session_state:
        st.session_state.attack_history = []
    
    col_ctrl, col_sim = st.columns([0.3, 0.7])
    
    with col_ctrl:
        st.markdown("**Attack Vector Matrix**")
        att_type = st.selectbox("Attack Type", list(ATTACKS.keys()))
        intensity = st.slider("Attack Intensity", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        sig_len = st.number_input("Signature Length", min_value=4, max_value=256, value=16, step=4)
        seed = st.number_input("Random Seed", min_value=0, max_value=9999, value=42)
        
        c1, c2 = st.columns(2)
        launch = c1.button("LAUNCH ATTACK", type="primary")
        reset = c2.button("RESET SIMULATION")
        
        if reset:
            st.session_state.current_attack_res = None
            st.session_state.attack_history = []
            st.rerun()

    with col_sim:
        if launch:
            start_t = time.perf_counter()
            with st.spinner(f"Initiating {att_type} execution pipeline..."):
                runner = AttackRunner(sig_length=sig_len, n_baseline=2, seed=seed)
                try:
                    runner._build_detector()
                except Exception:
                    pass
                
                AttClass = ATTACKS[att_type]
                attack_inst = AttClass(seed=seed)
                
                exec_start = time.perf_counter()
                res = runner.run_attack(
                    attack=attack_inst,
                    attack_type=att_type,
                    intensity=intensity
                )
                exec_end = time.perf_counter()
                
                res.latency = exec_end - start_t
                
                st.session_state.current_attack_res = res
                st.session_state.attack_history.append({
                    "Attack": att_type,
                    "Intensity": intensity,
                    "Anomaly Score": round(res.anomaly_score, 4),
                    "Classification": res.classification,
                    "Verification": round(res.verification_score, 4),
                    "Authorization": res.authorization_status,
                    "Detection": res.detection_status,
                    "Latency (s)": round(res.latency, 3)
                })

        # Render the WebGL Simulation Window
        current_res = st.session_state.get("current_attack_res")
        
        if current_res:
            attack_event = {
                "type": current_res.attack_metadata.name.upper(),
                "intensity": intensity,
                "classification": current_res.classification,
                "status": "RUNNING"
            }
            render_3d_simulation(attack_event)
        else:
            render_3d_simulation({"status": "NORMAL"})

    # Results Panel
    if current_res:
        st.divider()
        st.markdown("### Threat Detection Telemetry")
        
        c_stat, c_quant, c_sec, c_lat = st.columns(4)
        with c_stat:
            st.markdown("**ATTACK STATUS**")
            st.write(f"Type: `{current_res.attack_metadata.name}`")
            st.write(f"Intensity: `{intensity:.2f}`")
            st.write(f"Detection: `{current_res.detection_status}`")
            st.write(f"Authorizn: `{current_res.authorization_status}`")
            
        with c_quant:
            st.markdown("**QUANTUM METRICS**")
            st.write(f"Fidelity: `{current_res.teleportation_fidelity:.4f}`")
            st.write(f"Matches: `{current_res.measurement_statistics['matches']}/{current_res.measurement_statistics['total']}`")
            st.write(f"Verif Score: `{current_res.verification_score:.4f}`")
            
        with c_sec:
            st.markdown("**SECURITY METRICS**")
            st.write(f"Anomaly Score: `{current_res.anomaly_score:.4f}`")
            
            color = "red" if current_res.classification == "THREAT" else "orange" if current_res.classification == "SUSPICIOUS" else "green"
            st.markdown(f"Class: <span style='color:{color}; font-weight:bold;'>{current_res.classification}</span>", unsafe_allow_html=True)
            
        with c_lat:
            st.markdown("**LATENCY**")
            st.write(f"Exec Time: `{current_res.latency:.3f} s`")
            
        st.info(f"**Detector Reason**: {current_res.reason}")

    # Comparison Table
    if st.session_state.attack_history:
        st.divider()
        cA, cB = st.columns([0.85, 0.15])
        cA.markdown("### Attack Comparison History")
        if cB.button("Clear Results"):
            st.session_state.attack_history = []
            st.session_state.current_attack_res = None
            st.rerun()
            
        df = pd.DataFrame(st.session_state.attack_history)
        st.dataframe(df, use_container_width=True, hide_index=True)
