"""
dashboard/components/charts.py
==============================
Interactive chart components using Plotly and pre-computed datasets.
"""
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent.parent / "experiments" / "results"

def load_csv_safe(filename: str) -> pd.DataFrame:
    try:
        path = RESULTS_DIR / filename
        if path.exists():
            return pd.read_csv(path)
    except Exception:
        pass
    return pd.DataFrame()


def render_attack_comparison():
    """Render interactive attack detection comparison."""
    df = load_csv_safe("attack_metrics.csv")
    if df.empty:
        st.warning("Attack metrics data not available. (Run Phase 6.5 tests to generate).")
        return
        
    st.subheader("Attack-wise Detection Rate")
    # Need to filter or aggregate to get per-attack Detection Rate (TPR)
    # The dataframe might contain TPR per attack type.
    if "attack_type" in df.columns and "detection_rate" in df.columns:
        fig = px.bar(df, x="attack_type", y="detection_rate", color="detection_rate",
                     color_continuous_scale="reds", range_y=[0, 1],
                     title="Detection Effectiveness by Attack Type")
        fig.update_layout(template="plotly_dark", yaxis_tickformat=".1%")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.image(str(RESULTS_DIR / "attack_detection_comparison.png"), use_column_width=True)


def render_threshold_analysis():
    """Render interactive threshold vs FAR/FRR chart."""
    df = load_csv_safe("threshold_analysis.csv")
    if df.empty:
        st.warning("Threshold analysis data not available.")
        return
        
    if all(c in df.columns for c in ["threshold", "far", "frr", "detection_rate"]):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["threshold"], y=df["far"], name="False Acceptance Rate (FAR)", line=dict(color='red')))
        fig.add_trace(go.Scatter(x=df["threshold"], y=df["frr"], name="False Rejection Rate (FRR)", line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=df["threshold"], y=df["detection_rate"], name="Detection Rate", line=dict(color='green')))
        
        fig.update_layout(
            template="plotly_dark",
            title="System Threshold Tradeoffs",
            xaxis_title="Anomaly Threshold",
            yaxis_title="Rate",
            yaxis_tickformat=".1%",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Interactive threshold data structurally incompatible, viewing static render:")
        st.image(str(RESULTS_DIR / "roc_curve.png"))


def render_performance_analytics():
    """Render performance and scalability charts."""
    cols = st.columns(2)
    with cols[0]:
        st.markdown("**Signature Length Scalability**")
        df_sig = load_csv_safe("signature_scalability.csv")
        if not df_sig.empty and "signature_length" in df_sig.columns and "mean_end_to_end_time" in df_sig.columns:
            # converting s to ms
            df_sig['MeanLatency_ms'] = df_sig['mean_end_to_end_time'] * 1000
            fig1 = px.line(df_sig, x="signature_length", y="MeanLatency_ms", markers=True, title="Latency vs Signature Size")
            fig1.update_layout(template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            p = RESULTS_DIR / "signature_latency.png"
            if p.exists():
                st.image(str(p), use_column_width=True)
                
    with cols[1]:
        st.markdown("**Session Load Throughput**")
        df_sess = load_csv_safe("session_scalability.csv")
        if not df_sess.empty and "session_count" in df_sess.columns and "throughput_sessions_per_sec" in df_sess.columns:
            fig2 = px.line(df_sess, x="session_count", y="throughput_sessions_per_sec", markers=True, title="Throughput vs Concurrent Sessions")
            fig2.update_layout(template="plotly_dark")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            p = RESULTS_DIR / "session_throughput.png"
            if p.exists():
                st.image(str(p), use_column_width=True)
