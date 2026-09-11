"""
attacks/unauthorized_verification.py
=====================================
Unauthorized verification attack simulation.

Phase 5 -- SIH26141 | Blockchain & Cybersecurity.

Simulates a verifier attempting to verify a signature without valid
authorization/context.  Authorization state is represented explicitly
and the decision AUTHORIZED/UNAUTHORIZED is made independently of
the statistical anomaly score.

The unauthorized verifier lacks proper authorization tokens, resulting
in an immediate rejection regardless of whether the signature itself
is valid.

No AI/ML is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from attacks.base import AttackResult, BaseAttack, SessionMetadata
from utils.logger import get_logger

logger = get_logger(__name__)

__all__: list[str] = [
    "UnauthorizedVerificationAttack",
    "AuthorizationCheck",
    "check_authorization",
]


# ---------------------------------------------------------------------------
# Authorization check
# ---------------------------------------------------------------------------

@dataclass
class AuthorizationCheck:
    """Result of an explicit authorization check.

    Attributes
    ----------
    status : str
        'AUTHORIZED' or 'UNAUTHORIZED'.
    verifier_id : str
        Identity of the verifier.
    authorized_verifiers : list[str]
        List of verifier IDs that are authorized for this session.
    reason : str
        Human-readable explanation of the decision.
    """

    status: str = "UNAUTHORIZED"
    verifier_id: str = ""
    authorized_verifiers: list[str] = None  # type: ignore[assignment]
    reason: str = ""

    def __post_init__(self) -> None:
        if self.authorized_verifiers is None:
            self.authorized_verifiers = []

    @property
    def is_authorized(self) -> bool:
        return self.status == "AUTHORIZED"


def check_authorization(
    verifier_id: str,
    metadata: SessionMetadata,
    authorized_verifiers: Optional[List[str]] = None,
) -> AuthorizationCheck:
    """Check if a verifier is authorized for a session.

    Authorization is determined by:
    1. The metadata.authorized flag.
    2. The verifier_id being in the authorized_verifiers list.

    Parameters
    ----------
    verifier_id : str
        Identity of the verifier attempting verification.
    metadata : SessionMetadata
        Session metadata with authorization context.
    authorized_verifiers : list[str] or None
        List of authorized verifier IDs.  If None, uses
        [metadata.verifier_id] as the only authorized verifier.

    Returns
    -------
    AuthorizationCheck
    """
    if authorized_verifiers is None:
        authorized_verifiers = [metadata.verifier_id]

    if not metadata.authorized:
        return AuthorizationCheck(
            status="UNAUTHORIZED",
            verifier_id=verifier_id,
            authorized_verifiers=authorized_verifiers,
            reason=f"authorization_failure: session metadata marks "
                   f"authorization=False",
        )

    if verifier_id not in authorized_verifiers:
        return AuthorizationCheck(
            status="UNAUTHORIZED",
            verifier_id=verifier_id,
            authorized_verifiers=authorized_verifiers,
            reason=f"authorization_failure: verifier '{verifier_id}' "
                   f"not in authorized list {authorized_verifiers}",
        )

    return AuthorizationCheck(
        status="AUTHORIZED",
        verifier_id=verifier_id,
        authorized_verifiers=authorized_verifiers,
        reason=f"verifier '{verifier_id}' is authorized",
    )


# ---------------------------------------------------------------------------
# Unauthorized Verification Attack
# ---------------------------------------------------------------------------

class UnauthorizedVerificationAttack(BaseAttack):
    """Simulate an unauthorized verifier attempting verification.

    The attacker uses an unauthorized identity to attempt verification.
    The authorization check rejects the attempt independently of any
    statistical anomaly score.

    At intensity 0.0, no modification is made (verifier is authorized).
    At intensity > 0.0, the verifier identity is changed to an
    unauthorized one and/or the authorization flag is revoked.

    Parameters
    ----------
    seed : int
        Random seed for reproducibility.
    attacker_verifier_id : str
        Identity of the unauthorized verifier.
    """

    def __init__(
        self,
        seed: int = 42,
        attacker_verifier_id: str = "unauthorized_charlie",
    ) -> None:
        super().__init__(seed=seed)
        self._attacker_id = attacker_verifier_id

    def _execute_attack(
        self,
        statevectors: List[np.ndarray],
        metadata: SessionMetadata,
        intensity: float,
    ) -> AttackResult:
        """Set unauthorized verification context.

        Parameters
        ----------
        statevectors : list[np.ndarray]
            Legitimate statevectors (unchanged).
        metadata : SessionMetadata
            Session metadata to manipulate.
        intensity : float
            0.0 = no manipulation (authorized), > 0.0 = unauthorized.

        Returns
        -------
        AttackResult
        """
        evidence: list[str] = []
        indicators: dict = {
            "attacker_verifier_id": self._attacker_id,
            "legitimate_verifier_id": metadata.verifier_id,
            "authorization_revoked": False,
        }

        if intensity <= 0.0:
            evidence.append("intensity=0.0: no unauthorized verification applied")
            return AttackResult(
                statevectors=statevectors,
                metadata=metadata,
                evidence=evidence,
                attack_indicators=indicators,
                authorization_status="AUTHORIZED",
            )

        # Revoke authorization
        metadata.authorized = False
        metadata.verifier_id = self._attacker_id
        indicators["authorization_revoked"] = True

        auth_check = check_authorization(
            verifier_id=self._attacker_id,
            metadata=metadata,
        )

        evidence.append(
            f"authorization_failure: verifier '{self._attacker_id}' "
            f"is not authorized for session {metadata.session_id[:8]}..."
        )
        evidence.append(
            f"authorization_status: {auth_check.status} — {auth_check.reason}"
        )
        indicators["auth_check_result"] = auth_check.status

        return AttackResult(
            statevectors=statevectors,
            metadata=metadata,
            evidence=evidence,
            attack_indicators=indicators,
            authorization_status="UNAUTHORIZED",
        )
