"""Safety controls (Phase F): scope, Rules of Engagement, and approval gates.

The Master Agent consults this module before dispatching any task. Intrusive
Active Testing is never dispatched until an approval has been granted. Targets
are validated against scope and RoE; no target is ever hard-coded.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse

from ..errors import ApprovalDenied, ScopeViolation
from ..schemas import (
    ApprovalState,
    RulesOfEngagement,
    Scope,
    Target,
    new_id,
    utc_now,
)


@dataclass
class Approval:
    """A human approval record for a gated action."""

    capability: str
    approval_id: str = field(default_factory=lambda: new_id("approval"))
    target: str | None = None
    state: ApprovalState = ApprovalState.PENDING
    requested_action: str = ""
    decided_at: str | None = None
    schema_version: str = "1.0.0"


class ApprovalStore:
    """In-memory registry of approvals for one assessment."""

    def __init__(self) -> None:
        self._by_capability: dict[tuple[str, str | None], Approval] = {}

    def request(self, capability: str, target: str | None,
                requested_action: str) -> Approval:
        key = (capability, target)
        existing = self._by_capability.get(key)
        if existing is not None:
            return existing
        approval = Approval(
            capability=capability,
            target=target,
            requested_action=requested_action,
            state=ApprovalState.PENDING,
        )
        self._by_capability[key] = approval
        return approval

    def grant(self, capability: str, target: str | None = None) -> Approval:
        approval = self._by_capability.get((capability, target))
        if approval is None:
            approval = self.request(capability, target, f"grant {capability}")
        approval.state = ApprovalState.APPROVED
        approval.decided_at = utc_now()
        return approval

    def reject(self, capability: str, target: str | None = None) -> Approval:
        approval = self._by_capability.get((capability, target))
        if approval is None:
            approval = self.request(capability, target, f"reject {capability}")
        approval.state = ApprovalState.REJECTED
        approval.decided_at = utc_now()
        return approval

    def state_for(self, capability: str, target: str | None) -> ApprovalState:
        exact = self._by_capability.get((capability, target))
        if exact is not None:
            return exact.state
        wildcard = self._by_capability.get((capability, None))
        if wildcard is not None:
            return wildcard.state
        return ApprovalState.NOT_REQUIRED


def _host_of(value: str) -> str:
    if "://" in value:
        parsed = urlparse(value)
        return (parsed.hostname or "").lower()
    return value.split("/")[0].split(":")[0].lower()


def _matches(host: str, pattern: str) -> bool:
    pattern = pattern.lower()
    if pattern.startswith("*."):
        return host == pattern[2:] or host.endswith(pattern[1:])
    return host == pattern


class SafetyPolicy:
    """Scope, RoE, and approval enforcement."""

    def __init__(self, scope: Scope, roe: RulesOfEngagement) -> None:
        self._scope = scope
        self._roe = roe

    # -- scope / RoE -------------------------------------------------------

    def check_scope(self, target: Target) -> None:
        host = _host_of(target.value)
        if not host:
            raise ScopeViolation(f"target has no resolvable host: {target.value!r}")

        for pattern in self._scope.excluded_targets:
            if _matches(host, pattern):
                raise ScopeViolation(f"target {host} is explicitly excluded")

        included = self._scope.included_targets
        if included and not any(_matches(host, p) for p in included):
            raise ScopeViolation(f"target {host} is not within the included scope")

        allowed_hosts = self._roe.allowed_hosts
        if allowed_hosts and not any(_matches(host, p) for p in allowed_hosts):
            raise ScopeViolation(f"target {host} is not an allowed host under RoE")

        if "://" in target.value:
            scheme = urlparse(target.value).scheme.lower()
            if scheme and self._roe.allowed_protocols \
                    and scheme not in self._roe.allowed_protocols:
                raise ScopeViolation(f"protocol {scheme} is not permitted under RoE")

    # -- approval ----------------------------------------------------------

    def requires_approval(self, capability: str, intrusive: bool) -> bool:
        if intrusive:
            return True
        if capability in self._roe.approval_required_capabilities:
            return True
        return capability.startswith("active-testing.")

    def enforce_approval(self, capability: str, target: Target,
                         approvals: ApprovalStore) -> None:
        """Raise unless a required approval has been granted."""
        state = approvals.state_for(capability, target.value)
        if state == ApprovalState.APPROVED:
            return
        if state in (ApprovalState.REJECTED, ApprovalState.EXPIRED,
                     ApprovalState.CANCELLED):
            raise ApprovalDenied(
                f"approval for '{capability}' on {target.value} is {state.value}"
            )
        # PENDING or NOT_REQUIRED-but-required: block dispatch.
        raise ApprovalDenied(
            f"approval required for '{capability}' on {target.value} (state={state.value})"
        )
