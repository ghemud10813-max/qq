# Architecture Overivew

## System Design
The Quantum-Inspired Digital Signature (QDS) security detection framework is built as a real-time, hardware-agnostic digital signature scheme secured by fundamental quantum mechanics properties.
It consists of several core subsystems orchestrated via an event-driven `EndToEndPipeline`.

### Core Modules

1. **QDS Protocol Layer (`src/qds/`)**
   - **Signature Generation**: Translates large data blocks into quantum states constructed natively from the eigenstates of Pauli X, Y, and Z observable matrices.
   - **Verification**: Employs non-destructive projective measurements using simulated IBM Qiskit runtimes.

2. **Quantum Mechanics Kernel (`src/quantum/`)**
   - Models the creation of bell pairs natively.
   - Entangles particles for protocol-reliant teleportation execution.
   - Processes quantum channels with calibrated state-flip and depolarizing quantum error noise variables.

3. **Statistical Cyber Security (`src/security/`)**
   - **Fingerprinting**: Profiles incoming states to establish probabilistic norms (i.e. Mean Standard Deviation error margins) around an established signature pattern.
   - **Threshold Logic**: Computes an anomaly scale based on dynamic distance bounds (utilizing calibrated FAR/FRR boundaries).

4. **Attack Simulation (`src/attacks/`)**
   - Mocks the cyber kill chain (Forgery, Session Impersonation, unauthorized Replay).
   - Generates exact measurable anomalies that the anomaly detector trains and evaluates against.

### Teleportation Pipeline
All events flow synchronously through `pipeline.py`:
`Signature Generation -> Teleportation -> State Measurement -> Classical Verification -> Statistical Hardening`
