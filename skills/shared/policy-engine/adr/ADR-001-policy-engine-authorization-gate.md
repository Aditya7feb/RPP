# ADR-001 — Policy Engine Authorization Gate

**File:** `skills/shared/policy-engine/adr/ADR-001-policy-engine-authorization-gate.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform performs actions against real targets. Whether an
action is permitted depends on two independent concerns: the assessment
[Scope](../../../../schemas/scope.md) (what may be tested) and the
[Rules of Engagement](../../../../schemas/rules-of-engagement.md) (what actions
are permitted). Before this decision, scope and Rules of Engagement were inline,
free-form fields on the assessment, and there was no canonical component that
every capability consulted before acting.

Without a central authorization gate, the platform would suffer

- Each skill interpreting scope and Rules of Engagement independently and
  inconsistently
- No uniform enforcement that out-of-scope targets are never acted upon
- No consistent determination of when human approval is required
- No auditable record of authorization decisions
- Risk of intrusive actions executing without authorization

The platform requires a single, canonical, implementation-independent
authorization gate that every capability consults before acting.

---

# Decision

The platform SHALL provide a dedicated Policy Engine shared skill that
centralizes pre-action authorization behind a stable interface.

The Policy Engine SHALL

- Resolve the applicable [Scope](../../../../schemas/scope.md) and
  [Rules of Engagement](../../../../schemas/rules-of-engagement.md)
- Evaluate a proposed action against target scope and permitted actions
- Return one of `allow`, `deny`, or `requires_approval`
- Determine when an [Approval](../../../../schemas/approval.md) is required,
  without granting it
- Attach the Rules-of-Engagement rate ceiling to allow decisions for enforcement
  by the [Rate Limiter](../../rate-limiter/README.md)
- Record every decision as evidence conforming to the
  [Evidence schema](../../../../schemas/evidence.md)
- Fail closed: never yield an implicit allow

Every capability that acts against a target SHALL consult the Policy Engine
before acting. The Policy Engine SHALL NOT execute actions, grant approvals, or
enforce rate limits directly.

This decision is paired with the introduction of the canonical
[Scope](../../../../schemas/scope.md) and
[Rules of Engagement](../../../../schemas/rules-of-engagement.md) schemas, which
replace the previously inline assessment fields.

---

# Alternatives Considered

## Per-Skill Authorization

Each skill could interpret scope and Rules of Engagement itself.

Rejected because it produces inconsistent enforcement, no central audit, and a
high risk of an out-of-scope or unauthorized action slipping through.

## Embedding Authorization In The Workflow Runtime

Authorization could live inside the workflow runtime.

Rejected because authorization is required by every capability, including those
invoked outside a workflow. A dedicated, reusable gate keeps the runtime focused
on orchestration while every consumer shares one authorization contract.

## Fail-Open On Uncertainty

The engine could allow actions when policy is ambiguous or unavailable.

Rejected because acting without proven authorization can harm targets and violate
engagement scope. The engine SHALL fail closed.

---

# Consequences

## Positive

- Uniform, central, auditable authorization for every action
- Guaranteed prevention of out-of-scope actions
- Consistent determination of approval requirements
- Clear separation of Scope (targets) from Rules of Engagement (actions)
- Deny-by-default safety

## Negative

- Every capability MUST consult the Policy Engine before acting
- An additional shared dependency is introduced
- Policy evaluation adds a step before each target-facing action

The negative consequences are outweighed by the safety and consistency benefits.

---

# Compliance

Consumers SHALL

- Consult the Policy Engine before every target-facing action
- Pass the action class and intrusiveness accurately
- Honor `requires_approval` by routing to the approval process
- Attach the returned ceiling to outbound operations
- Never treat an error or uncertain outcome as an allow

The workflow runtime and all domain skills SHALL depend on the Policy Engine and
SHALL NOT interpret scope or Rules of Engagement independently.

---

# Future Compatibility

Future versions MAY add decision explanation traces, per-action-class overlays,
and time-boxed grants. These extensions SHALL preserve the existing interface and
SHALL maintain backward compatibility and the fail-closed guarantee.

---

# Related Documents

- [Policy Engine README](../README.md)
- [Policy Engine Interface](../interface.md)
- [Policy Engine Execution Model](../execution.md)
- [Policy Engine Error Model](../error-model.md)
- [Scope Schema](../../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../../schemas/rules-of-engagement.md)
- [Approval Schema](../../../../schemas/approval.md)
- [Evidence Schema](../../../../schemas/evidence.md)
