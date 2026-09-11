# Security Model

The security model of our Quantum-Inspired Digital Signature (QDS) Framework defines the security assumptions, trust boundaries, and threat capabilities modeled and defended against by our anomaly detection layers.

## Fundamental Security Posture
Instead of relying strictly on computationally hard boundaries (e.g. RSA, ECC), this protocol bounds security physically using the **No-Cloning Theorem** and the **Observer Effect** intrinsic to quantum physics.

### Verification Paradigms
1. **Classical Hardening**: The QDS state acts as a one-time pad (OTP). When the threshold drops below the hard limit (e.g. `0.70`), standard authentication instantly triggers a REJECT.
2. **Statistical Hardening**: Because true quantum states suffer from decoherence, we cannot strictly reject every mismatch. Thus, the real evaluation analyzes the **pattern** of mismatches vs expected system hardware noise levels. An anomaly score > `warning` limit throws `SUSPICIOUS`; crossing `critical` throws `THREAT`.

### Trust Boundaries
* **Sender (Alice)**: Fully trusted. Holds the ability to generate eigenstates properly initialized by a true random seed.
* **Quantum Channel**: Fully UNTRUSTED. Open to MITM, Eavesdropping, and hardware noise. Modeled as a depolarizing channel.
* **Receiver (Bob)**: Trusted to perform faithful projective measurements.

## Resilience against FAR/FRR Overlap
To combat realistic noise without opening windows for forgery, the system runs a pre-calibration phase. By testing the distribution of standard noise across `N=10` calibration datasets, a 95th-percentile curve is generated dynamically ensuring an aggressive FRR (False Rejection Rate) < 4%, whilst containing the False Acceptance Rate (FAR) entirely.
