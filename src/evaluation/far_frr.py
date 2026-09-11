"""
evaluation/far_frr.py
=====================
False Acceptance Rate (FAR) and False Rejection Rate (FRR) computation.

Implements from Phase 7. Sweeps detection thresholds to build FAR/FRR
curves and locate the Equal Error Rate (EER) operating point.

    FAR = FP / (FP + TN)   — rate of accepting forged/attack signatures
    FRR = FN / (FN + TP)   — rate of rejecting legitimate signatures
    EER — threshold where FAR == FRR

No AI/ML — computed from threshold sweeps over simulation results.

Phase 0 status: stub only — no implementation.
"""

from __future__ import annotations

__all__: list[str] = ["compute_far", "compute_frr", "compute_eer"]


def compute_far() -> None:
    """Compute False Acceptance Rate at a given threshold.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("far_frr.compute_far — implemented in Phase 7.")


def compute_frr() -> None:
    """Compute False Rejection Rate at a given threshold.

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("far_frr.compute_frr — implemented in Phase 7.")


def compute_eer() -> None:
    """Compute Equal Error Rate (FAR == FRR operating point).

    Raises
    ------
    NotImplementedError
        Until Phase 7 is implemented.
    """
    raise NotImplementedError("far_frr.compute_eer — implemented in Phase 7.")
