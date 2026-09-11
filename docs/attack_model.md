# Cyber Attack Model

Our simulation framework verifies protocol integrity against a cyber killchain specifically designed for quantum telemetry and digital signatures. We evaluate against five primary attack vectors:

## 1. Forgery Attack
**Vector**: An adversary attempts to forge a signature state without the correct random initialization parameters. 
**Mechanics**: Generates completely unentangled and random Pauli eigenstates. 
**Detection**: Highly susceptible to standard Classical Verification due to severe eigenstate mismatch, triggering high-severity `THREAT` profiles instantly.

## 2. Session Impersonation
**Vector**: The adversary captures the signature ID and attempts to wrap it in a mock session with valid formatting.
**Mechanics**: Mismatches the intrinsic classical state properties mapped against the quantum representation. 
**Detection**: Triggers sudden shifts in `variance` and `entropy` statistical metrics inside our ThreatDetector kernel.

## 3. Replay Attack
**Vector**: A valid signature is captured and transmitted repeatedly to spoof multiple legitimate authorizations.
**Mechanics**: Re-uses the previous teleportation results.
**Detection**: Defeated mathematically by analyzing the standard deviation curve. Replayed packets feature almost `0.0` distribution deviance across evaluations because they bypass natural quantum depolarization—yielding a sudden and definitive statistical anomaly.

## 4. Unauthorized Verification
**Vector**: An actor forces signature verification requests prematurely or from an unauthorized terminal scope.
**Mechanics**: Intercepts the message payload but fails to coordinate the quantum teleportation channel resulting in a fidelity crash.
**Detection**: Caught via Teleportation Fidelity Metrics dropping beneath strict validation thresholds prior to classical measurement.

## 5. Channel Manipulation (Eavesdropping / MITM)
**Vector**: Attackers probe the active teleportation bus, triggering wave-function state collapse (the Observer Effect).
**Mechanics**: Forces a massive injection of noise into the operational qubits.
**Detection**: The detector notices an immense spike in depolarization characteristics (anomalous drop in Fidelity and increase in general bit-flip errors), cleanly isolating MITM events from background systemic hardware noise.
