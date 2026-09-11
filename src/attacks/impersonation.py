"""
attacks/impersonation.py
========================
Signer impersonation attack simulation.

Phase 5 -- SIH26141 | Blockchain & Cybersecurity.

Simulates an unauthorized signer attempting to act as a legitimate
participant.  The impersonator generates their own signature using a
different seed (different key material), producing a mismatched state
sequence that is distinguishable through verification statistics.

The impersonator's identity context is explicitly tracked so that
detection can identify identity/context mismatch as the reason.

No AI/ML is used.
"""

from __future__ import annotations

from typing import List

import numpy as np

from attacks.base import AttackResult, BaseAttack, SessionMetadata
from qds.pauli_states import EIGENSTATE_LABELS, get_eigenstate
from utils.logger import get_logger

logger = get_logger(__name__)

__all__: list[str] = ["ImpersonationAttack"]


class ImpersonationAttack(BaseAttack):
    """Simulate signer impersonation using unauthorized key material.

    The impersonator generates a completely different signature sequence
    using their own seed, then replaces a controlled fraction of the
    legitimate statevectors with their own.  At intensity 1.0, all
    elements are replaced with the impersonator's states.

    Parameters
    ----------
    seed : int
        Random seed for reproducibility.
    impersonator_id : str
        Identity string for the impersonator.
    """

    def __init__(self, seed: int = 42, impersonator_id: str = "attacker_eve") -> None:
        super().__init__(seed=seed)
        self._impersonator_id = impersonator_id

    def _execute_attack(
        self,
        statevectors: List[np.ndarray],
        metadata: SessionMetadata,
        intensity: float,
    ) -> AttackResult:
        """Replace statevectors with impersonator's key material.

        Parameters
        ----------
        statevectors : list[np.ndarray]
            Deep copies of legitimate statevectors.
        metadata : SessionMetadata
            Session metadata (signer_id will be changed).
        intensity : float
            Fraction of elements to replace.  0.0 = none, 1.0 = all.

        Returns
        -------
        AttackResult
        """
        n = len(statevectors)
        n_impersonate = max(0, int(round(n * intensity)))
        evidence: list[str] = []
        indicators: dict = {
            "n_impersonated": n_impersonate,
            "n_total": n,
            "impersonator_id": self._impersonator_id,
            "legitimate_signer_id": metadata.signer_id,
            "impersonate_fraction": n_impersonate / n if n > 0 else 0.0,
            "impersonated_positions": [],
        }

        if n_impersonate == 0:
            evidence.append("intensity=0.0: no impersonation applied")
            return AttackResult(
                statevectors=statevectors,
                metadata=metadata,
                evidence=evidence,
                attack_indicators=indicators,
            )

        # Generate impersonator's own state sequence with a different seed
        imp_rng = np.random.default_rng(self._seed + 9999)
        labels = list(EIGENSTATE_LABELS)
        imp_indices = imp_rng.integers(0, len(labels), size=n)
        imp_states = [get_eigenstate(labels[int(idx)]).statevector.copy()
                      for idx in imp_indices]

        # Replace a fraction of positions with impersonator states
        positions = self._rng.choice(n, size=n_impersonate, replace=False)
        positions.sort()

        for pos in positions:
            statevectors[int(pos)] = imp_states[int(pos)]
            indicators["impersonated_positions"].append(int(pos))
            evidence.append(
                f"identity_mismatch: position {int(pos)} replaced "
                f"with impersonator ({self._impersonator_id}) state"
            )

        # Update metadata to reflect impersonation
        metadata.signer_id = self._impersonator_id
        evidence.append(
            f"identity_context_mismatch: signer_id changed from "
            f"'{indicators['legitimate_signer_id']}' to '{self._impersonator_id}'"
        )
        evidence.append(
            f"impersonation_summary: {n_impersonate}/{n} elements replaced "
            f"({100.0 * n_impersonate / n:.1f}%)"
        )

        return AttackResult(
            statevectors=statevectors,
            metadata=metadata,
            evidence=evidence,
            attack_indicators=indicators,
        )
