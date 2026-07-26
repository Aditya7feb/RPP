# WebSocket API Security Skill Error Model

**File:** `skills/api-security/websocket/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the WebSocket API Security
Skill and their mapping to outcomes. Errors are deterministic and implementation
independent.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target or Asset outside Scope | rejected |
| policy-denied | Policy Engine denied the action | suppressed |
| approval-required | Action requires approval | awaiting_approval |
| identities-unavailable | Controlled identities not provided | partial |
| origins-unavailable | Allowed Origins not provided | partial |
| handshake-error | WebSocket Client could not complete the handshake | retry-or-partial |
| unreachable-target | Target did not respond | inconclusive |
| ambiguous-signal | Behavior insufficient to confirm a weakness | inconclusive |

---

# out-of-scope

When `target` or a referenced Asset is outside
[Scope](../../../schemas/scope.md), the skill SHALL reject the assessment before any
target-facing action.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) returns `deny`, the
skill SHALL suppress the action and record the decision in `decision_summary`.

---

# approval-required

When the decision is `requires_approval`, the skill SHALL defer the action to an
`awaiting_approval` state and SHALL NOT proceed until approval is granted.

---

# identities-unavailable

When message authorization checks require two controlled identities and fewer are
provided, the skill SHALL skip those checks and report them as not performed rather
than guessing.

---

# origins-unavailable

When the set of allowed Origins is not provided, Origin validation analysis MAY be
limited. The skill SHALL report the affected check as partial.

---

# handshake-error

When the [WebSocket Client](../../shared/websocket-client/README.md) cannot complete a
handshake, the skill MAY retry within policy limits. Persistent failure SHALL yield a
partial result.

---

# unreachable-target

When the target does not respond, affected checks SHALL be inconclusive.

---

# ambiguous-signal

When observed behavior is insufficient to confirm a weakness, the skill SHALL record
the result as inconclusive rather than emitting a Finding.

---

# Evidence On Error

The skill SHALL record Evidence for suppressed, deferred, partial, and inconclusive
outcomes to preserve auditability. Sensitive content SHALL be redacted.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
