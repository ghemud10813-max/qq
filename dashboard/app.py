"""
dashboard/app.py
================
Main entry point for the Quantum-Inspired Security Dashboard (Phase 8).
"""
import sys
from pathlib import Path
import streamlit as st

# Inject src into Python path to allow seamless imports of src/ modules
src_path = Path(__file__).parent.parent / "src"
root_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from dashboard.components import metrics
from dashboard.components import charts
from dashboard.components import quantum_view
from dashboard.components import attack_panel
from dashboard.components import security_panel
from dashboard.components import intro_simulation

# ---------------------------------------------------------------------------
# Dashboard Initialization
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="QVeris Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimalistic dark cybersecurity UI theme overrides
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}
.st-emotion-cache-1wivap2 {
    color: #00FF41;
}
</style>
""", unsafe_allow_html=True)


def main():
    st.title("QVeris")
    st.caption("Quantum-Inspired Threat Detection & Security Analytics")
    
    intro_simulation.render_intro()
    
    # Initialize basic session state vars for simulated logging
    if "event_logs" not in st.session_state:
        st.session_state.event_logs = []
        
    metrics.render_top_kpis()
    
    tab_overview, tab_verify, tab_attacks, tab_analytics, tab_quantum = st.tabs([
        "Overview & Performance",
        "Live Verification",
        "Attack Simulation",
        "Threshold Analytics",
        "Quantum Noise"
    ])
    
    with tab_overview:
        charts.render_attack_comparison()
        st.divider()
        metrics.render_event_log()
        
    with tab_verify:
        security_panel.render_verification_panel()
        
    with tab_attacks:
        attack_panel.render_attack_panel()
        
    with tab_analytics:
        st.subheader("Threshold Analysis (FAR/FRR)")
        charts.render_threshold_analysis()
        st.divider()
        st.subheader("Performance & Scalability")
        charts.render_performance_analytics()
        
    with tab_quantum:
        quantum_view.render_quantum_noise_panel()

if __name__ == "__main__":
    main()
