"""
quantum/noise_models.py
=======================
Quantum noise channel models for realistic simulation.

Implements from Phase 2.5. Wraps Qiskit Aer's ``NoiseModel`` to expose:
    - Depolarising channel
    - Bit-flip channel
    - Phase-flip channel
    - Combined (depolarising + measurement error) channel

Noise models are injected into Aer simulator jobs to study their impact on
QDS fidelity and threat detection thresholds.

Phase 0 status: stub only — no implementation.
No AI/ML libraries used.
"""

from __future__ import annotations

__all__: list[str] = [
    "depolarising_model",
    "bit_flip_model",
    "phase_flip_model",
    "combined_model",
]


def depolarising_model() -> None:  # -> NoiseModel (Phase 2.5)
    """Build a single-qubit depolarising noise model.

    Raises
    ------
    NotImplementedError
        Until Phase 2.5 is implemented.
    """
    raise NotImplementedError(
        "noise_models.depolarising_model — implemented in Phase 2.5."
    )


def bit_flip_model() -> None:
    """Build a single-qubit bit-flip noise model.

    Raises
    ------
    NotImplementedError
        Until Phase 2.5 is implemented.
    """
    raise NotImplementedError(
        "noise_models.bit_flip_model — implemented in Phase 2.5."
    )


def phase_flip_model() -> None:
    """Build a single-qubit phase-flip noise model.

    Raises
    ------
    NotImplementedError
        Until Phase 2.5 is implemented.
    """
    raise NotImplementedError(
        "noise_models.phase_flip_model — implemented in Phase 2.5."
    )


def combined_model() -> None:
    """Build a combined depolarising + measurement error noise model.

    Raises
    ------
    NotImplementedError
        Until Phase 2.5 is implemented.
    """
    raise NotImplementedError(
        "noise_models.combined_model — implemented in Phase 2.5."
    )
