# Quantum-Inspired Cyber Threat Detection for Digital Signature Security

**SIH26141 — Blockchain & Cybersecurity**

---

## Problem Statement & Objective

Digital signatures are a cornerstone of blockchain and cybersecurity infrastructure, providing authenticity and non-repudiation guarantees. Classical digital signatures face growing threats from forgery, impersonation, replay, and channel-manipulation attacks — threats that will intensify as quantum computers mature.

This project builds a **Quantum-Inspired Cyber Threat Detection** system that:

1. Implements a **Quantum Digital Signature (QDS)** scheme using Pauli eigenstates and quantum measurement.
2. Detects cyber threats against the QDS protocol using **quantum measurement statistics, mathematical divergence metrics, and threshold-based anomaly detection** — with **no AI/ML whatsoever**.
3. Simulates a comprehensive set of attacks and evaluates detection performance via FAR/FRR, fidelity, and throughput benchmarks.

---

## ⚠️ No AI/ML

> **This project contains zero AI or machine learning.**
> All threat detection is based entirely on quantum measurement statistics,
> Pauli basis probabilities, Shannon entropy, Hellinger distance,
> KL divergence, and mathematical thresholds.
> No TensorFlow, PyTorch, scikit-learn, or any other ML framework is used.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        main.py  (entry point)                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  ┌──────────┐       ┌──────────┐       ┌──────────────┐
  │ quantum/ │       │  qds/    │       │  security/   │
  │          │       │          │       │              │
  │ Bell     │──────▶│ keygen   │──────▶│ statistics   │
  │ states   │       │ signer   │       │ fingerprints │
  │ teleport │       │ verifier │       │ anomaly      │
  │ noise    │       │ scheme   │       │ thresholds   │
  │ Pauli    │       └──────────┘       │ detector     │
  │ measure  │                          └──────┬───────┘
  └──────────┘                                 │
                                               ▼
                        ┌──────────────────────────────────┐
                        │           attacks/               │
                        │  forgery · impersonation · replay│
                        │  unauthorized_verify · channel   │
                        └──────────────┬───────────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────────┐
                        │          evaluation/             │
                        │  fidelity · FAR/FRR · metrics   │
                        │  latency · performance           │
                        └──────────────────────────────────┘
                                       │
                        ┌──────────────┴───────────────────┐
                        │           dashboard/             │
                        │  real-time visualisation (Ph 8)  │
                        └──────────────────────────────────┘

              utils/  ←  config · logger · reproducibility · validation
              config/ ←  quantum_config.yaml · settings.py
```

---

## Technology Stack

| Component | Library / Tool |
|---|---|
| Quantum circuits & gates | [Qiskit](https://qiskit.org/) ≥ 1.0 |
| Quantum simulation | [Qiskit Aer](https://qiskit.github.io/qiskit-aer/) ≥ 0.14 |
| Numerical computing | NumPy ≥ 1.26 |
| Statistical analysis | SciPy ≥ 1.12 |
| Data management | Pandas ≥ 2.2 |
| Visualisation | Matplotlib ≥ 3.8 |
| Testing | pytest ≥ 8.0 |
| Configuration | PyYAML ≥ 6.0 |
| Python | ≥ 3.10 |

**No AI/ML frameworks (TensorFlow, PyTorch, scikit-learn) are present.**

---

## Project Structure

```
quantum-threat-detection/
├── src/
│   ├── quantum/                 # Bell states, teleportation, noise, Pauli, measurement
│   │   ├── __init__.py
│   │   ├── bell_states.py       # Phase 1
│   │   ├── teleportation.py     # Phase 2
│   │   ├── noise_models.py      # Phase 2.5
│   │   ├── pauli_states.py      # Phase 3
│   │   └── measurements.py      # Phase 3
│   ├── qds/                     # Quantum Digital Signature scheme
│   │   ├── __init__.py
│   │   ├── keygen.py            # Phase 3
│   │   ├── signer.py            # Phase 3
│   │   ├── verifier.py          # Phase 3
│   │   └── scheme.py            # Phase 3
│   ├── security/                # Statistical threat detection (no ML)
│   │   ├── __init__.py
│   │   ├── statistics.py        # Phase 4
│   │   ├── fingerprints.py      # Phase 4
│   │   ├── anomaly_scores.py    # Phase 4
│   │   ├── thresholds.py        # Phase 4
│   │   └── detector.py          # Phase 4
│   ├── attacks/                 # Attack simulations
│   │   ├── __init__.py
│   │   ├── forgery.py           # Phase 5
│   │   ├── impersonation.py     # Phase 5
│   │   ├── replay.py            # Phase 5
│   │   ├── unauthorized_verify.py  # Phase 5
│   │   └── channel_manipulation.py # Phase 5
│   ├── evaluation/              # Performance & security evaluation
│   │   ├── __init__.py
│   │   ├── fidelity.py          # Phase 7
│   │   ├── far_frr.py           # Phase 7
│   │   ├── metrics.py           # Phase 7
│   │   ├── latency.py           # Phase 7
│   │   └── performance.py       # Phase 7
│   └── utils/                   # Shared utilities (active from Phase 0)
│       ├── __init__.py
│       ├── config.py            # ConfigLoader (YAML → typed properties)
│       ├── logger.py            # get_logger factory
│       ├── reproducibility.py   # set_seed, get_rng, get_run_context
│       └── validation.py        # Input validators (basis, shots, qubits)
├── tests/
│   └── test_phase0.py           # Phase 0 test suite
├── experiments/                 # Experiment scripts (Phase 1+)
├── dashboard/                   # Real-time visualisation (Phase 8)
├── docs/                        # Technical documentation
├── config/
│   ├── __init__.py
│   ├── quantum_config.yaml      # Master YAML configuration
│   └── settings.py              # Compiled Python-level defaults
├── main.py                      # Entry point
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

---

## Development Roadmap

| Phase | Title | Status |
|---|---|---|
| **0** | Foundation — project structure, config, utils, stubs | ✅ Complete |
| 1 | Bell States & Entanglement | ✅ Complete |
| 2 | Teleportation & Fidelity | ✅ Complete |
| 2.5 | Quantum Noise Models | ✅ Complete |
| 3 | QDS + Pauli Eigenstates | ✅ Complete |
| 4 | Statistical Threat Detection | ✅ Complete |
| 5 | Attack Simulation | ✅ Complete |
| 6 | Security Analysis | ✅ Complete |
| 7 | Performance Evaluation | ✅ Complete |
| 8 | Dashboard | ✅ Complete |
| 9 | Final Integration | ✅ Complete |

---

## Installation

### Prerequisites

- Python ≥ 3.10
- pip or a virtual environment manager

### Setup

```bash
# Clone / enter the project
cd quantum-threat-detection

# Create and activate virtual environment
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Install project in editable mode (enables src-based imports)
pip install -e .
```

---

## Running the Application

```bash
# Phase 0 environment check
python main.py

# With a custom seed
python main.py --seed 123

# With a custom config file
python main.py --config path/to/my_config.yaml
```

---

## Testing

The test suite uses **pytest**. The `pythonpath = ["src"]` setting in
`pyproject.toml` ensures all `src`-based imports resolve correctly.

```bash
# Run the full Phase 0 test suite
pytest tests/test_phase0.py -v

# Run with coverage
pytest tests/test_phase0.py -v --cov=src --cov-report=term-missing

# Run all tests
pytest -v
```

### Phase 0 Test Coverage

| Test | Verifies |
|---|---|
| `test_package_imports` | All six src sub-packages import without error |
| `test_configuration_loading` | ConfigLoader reads YAML and returns correct typed values |
| `test_config_defaults` | seed=42, shots=1024, backend=aer_simulator |
| `test_measurement_bases` | X/Y/Z bases present in config |
| `test_reproducible_numpy_seed` | Same seed → same NumPy random draws |
| `test_get_rng_reproducibility` | `get_rng(42)` produces identical sequences |
| `test_qiskit_circuit_creation` | QuantumCircuit(2) builds and has 2 qubits |
| `test_aer_simulator_available` | AerSimulator instantiates and runs a simple circuit |
| `test_validate_basis_valid` | All of x/y/z/X/Y/Z pass validation |
| `test_validate_basis_invalid` | Invalid bases raise ValueError |
| `test_validate_shots_valid` | Positive integers pass |
| `test_validate_shots_invalid` | Zero and negatives raise ValueError |
| `test_phase_flags` | Phase 0 enabled; Phase 1+ disabled |

---

## Reproducibility

All randomness in the project is controlled through a single seed, set via:

```python
from utils.reproducibility import set_seed
set_seed(42)   # seeds Python random, NumPy legacy state, NumPy Generator
```

The seed is stored in `config/quantum_config.yaml` and can be overridden
at runtime with `python main.py --seed <N>`.

Qiskit Aer jobs will be seeded per-execution in Phase 1+ using the same
seed value propagated through `ConfigLoader.random_seed`.

---

## Configuration Reference

Edit `config/quantum_config.yaml` to change project-wide settings:

```yaml
random_seed: 42
simulator:
  backend: "aer_simulator"
  shots: 1024
measurement_bases:
  X: "x"
  Y: "y"
  Z: "z"
logging:
  level: "INFO"
```

All settings are also accessible as typed Python constants in
`config/settings.py` and via `ConfigLoader` typed properties.

---

## Contributing

This is a research project for SIH26141. Follow the phase roadmap strictly —
do not implement Phase N+1 code until Phase N is complete and tested.

---

## License

MIT — see `LICENSE` (to be added).
