# Quantum-Inspired Digital Signature Security Dashboard

This dashboard provides a polished, interactive, real-time visualization of the Quantum-Inspired Cyber Threat Detection system, covering verification, security analysis, quantum visualization, and threat performance.

## Setup
Install the necessary requirements:
```bash
pip install streamlit plotly
```

## Running the Dashboard
Run the following from the root of the project:
```bash
streamlit run dashboard/app.py
```

## Architecture
- **`app.py`**: The main entry point combining components into a professional layout.
- **`components/`**: Modular layout sections.
    - **`metrics.py`**: Top-level KPI metrics and system statuses.
    - **`charts.py`**: Analytics graphs loading data from `experiments/results`.
    - **`quantum_view.py`**: Noise and fidelity visualizations using Phase 2/3 utilities.
    - **`attack_panel.py`**: Live attack generation using Phase 5 utilities.
    - **`security_panel.py`**: Live signature and verification tests using Phase 4/6 logic.

## Limitations
- No true quantum hardware is used; simulations depend on `qiskit_aer`.
- Real-time simulations might be demanding on memory for extremely high session depths.
