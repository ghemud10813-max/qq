"""
attacks/forgery.py
==================
Quantum signature forgery attack simulation.

Phase 5 -- SIH26141 | Blockchain & Cybersecurity.

Simulates an attacker attempting to create/alter a valid QDS signature
without the legitimate signature information.  The attacker replaces
a controlled fraction of statevectors with randomly-chosen Pauli
eigenstates, simulating a forgery attempt.

Controlled signature-state substitutions:
- intensity 0.0 → no modification (identity)
- intensity 1.0 → all elements replaced with random eigenstates

The resulting measurements are processed by the Phase 4 detector,
which flags the statistical deviation from the legitimate baseline.

No AI/ML is used.
"""

from __future__ import annotations

from typing import List

import numpy as np

from attacks.base import AttackResult, BaseAttack, SessionMetadata
from qds.pauli_states import EIGENSTATE_LABELS, get_eigenstate
from utils.logger import get_logger

logger = get_logger(__name__)

__all__: list[str] = ["ForgeryAttack"]


class ForgeryAttack(BaseAttack):
    """Simulate signature forgery by substituting statevectors.

    The attacker replaces a fraction of the signature's statevectors
    with randomly-chosen Pauli eigenstates (from a uniform distribution
    over the six eigenstates).  This mimics an adversary who does not
    know the signer's key material and guesses randomly.

    Parameters
    ----------
    seed : int
        Random seed for reproducibility.
    """

    def _execute_attack(
        self,
        statevectors: List[np.ndarray],
        metadata: SessionMetadata,
        intensity: float,
    ) -> AttackResult:
        """Replace a controlled fraction of statevectors with random eigenstates.

        Parameters
        ----------
        statevectors : list[np.ndarray]
            Deep copies of legitimate statevectors.
        metadata : SessionMetadata
            Session metadata (not modified by forgery).
        intensity : float
            Fraction of elements to forge.  0.0 = none, 1.0 = all.

        Returns
        -------
        AttackResult
        """
        n = len(statevectors)
        n_forge = max(0, int(round(n * intensity)))
        evidence: list[str] = []
        indicators: dict = {
            "n_forged": n_forge,
            "n_total": n,
            "forge_fraction": n_forge / n if n > 0 else 0.0,
            "forged_positions": [],
        }

        if n_forge == 0:
            evidence.append("intensity=0.0: no forgery applied")
            return AttackResult(
                statevectors=statevectors,
                metadata=metadata,
                evidence=evidence,
                attack_indicators=indicators,
            )

        # Randomly select which positions to forge
        positions = self._rng.choice(n, size=n_forge, replace=False)
        positions.sort()

        labels = list(EIGENSTATE_LABELS)
        for pos in positions:
            # Pick a random eigenstate (attacker doesn't know the correct one)
            idx = int(self._rng.integers(0, len(labels)))
            forged_label = labels[idx]
            forged_state = get_eigenstate(forged_label)
            statevectors[int(pos)] = forged_state.statevector.copy()
            indicators["forged_positions"].append(int(pos))
            evidence.append(
                f"signature_mismatch: position {int(pos)} forged "
                f"with random eigenstate {forged_label}"
            )

        evidence.append(
            f"forgery_summary: {n_forge}/{n} elements replaced "
            f"({100.0 * n_forge / n:.1f}%)"
        )

        return AttackResult(
            statevectors=statevectors,
            metadata=metadata,
            evidence=evidence,
            attack_indicators=indicators,
        )
