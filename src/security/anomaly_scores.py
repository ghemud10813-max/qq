"""
security/anomaly_scores.py
==========================
Anomaly scoring functions based on statistical divergence.

Implements from Phase 4. Scores quantify how much an observed measurement
distribution deviates from an expected (legitimate) baseline using:
    - Total Variation Distance
    - Kullback-Leibler Divergence
    - Bhattacharyya Coefficient
    - Chi-squared statistic

Higher scores → greater anomaly → potential threat.
No AI/ML — purely mathematical metrics.

Phase 0 status: stub only — no implementation.
"""

from __future__ import annotations

__all__: list[str] = [
    "total_variation_distance",
    "kl_divergence",
    "bhattacharyya_coefficient",
    "chi_squared_score",
]


def total_variation_distance() -> None:
    """Compute Total Variation Distance between two distributions.

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("anomaly_scores.total_variation_distance — Phase 4.")


def kl_divergence() -> None:
    """Compute Kullback-Leibler divergence D_KL(P || Q).

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("anomaly_scores.kl_divergence — Phase 4.")


def bhattacharyya_coefficient() -> None:
    """Compute Bhattacharyya coefficient between two distributions.

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("anomaly_scores.bhattacharyya_coefficient — Phase 4.")


def chi_squared_score() -> None:
    """Compute chi-squared statistic between observed and expected counts.

    Raises
    ------
    NotImplementedError
        Until Phase 4 is implemented.
    """
    raise NotImplementedError("anomaly_scores.chi_squared_score — Phase 4.")
