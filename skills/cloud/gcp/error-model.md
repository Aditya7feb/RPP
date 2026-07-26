# GCP Cloud Security Skill Error Model

**File:** `skills/cloud/gcp/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the GCP Cloud Security Skill and
their mapping to outcomes. Errors are deterministic and implementation independent.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Project or resource outside Scope | rejected |
| policy-denied | Policy Engine denied the action | suppressed |
| approval-required | Action requires approval | awaiting_approval |
| credentials-unavailable | Read credentials not provided | partial |
| metadata-unavailable | Provider metadata could not be collected | partial |
| ambiguous-signal | Metadata insufficient to confirm a weakness | inconclusive |

---

# out-of-scope

When the target or a referenced Asset is outside [Scope](../../../schemas/scope.md), the
skill SHALL reject the assessment before any target-facing action.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) returns `deny`, the skill
SHALL suppress the action and record the decision.

---

# approval-required

When the decision is `requires_approval`, the skill SHALL defer the action to an
`awaiting_approval` state.

---

# credentials-unavailable

When read credentials are not provided, affected checks SHALL be reported as not performed
rather than guessed.

---

# metadata-unavailable

When the GCP or Cloud Storage client cannot collect metadata, affected checks SHALL be
partial.

---

# ambiguous-signal

When observed metadata is insufficient to confirm a weakness, the skill SHALL record the
result as inconclusive rather than emitting a Finding.

---

# Evidence On Error

The skill SHALL record Evidence for suppressed, deferred, partial, and inconclusive
outcomes to preserve auditability. Sensitive values SHALL be redacted.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
