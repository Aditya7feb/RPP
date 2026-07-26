# Terraform Cloud Security Skill Error Model

**File:** `skills/cloud/terraform/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Terraform Cloud Security Skill
and their mapping to outcomes. Errors are deterministic and implementation independent.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Configuration root outside Scope | rejected |
| policy-denied | Policy Engine denied the action | suppressed |
| approval-required | Action requires approval | awaiting_approval |
| configuration-unavailable | Configuration files could not be read | partial |
| parse-incomplete | Configuration could not be fully interpreted | partial |
| ambiguous-signal | Configuration insufficient to confirm a weakness | inconclusive |

---

# out-of-scope

When the target or configuration root is outside [Scope](../../../schemas/scope.md), the
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

# configuration-unavailable

When the Filesystem Client cannot read configuration, affected checks SHALL be partial.

---

# parse-incomplete

When configuration cannot be fully interpreted, the skill SHALL record a partial result
rather than guessing.

---

# ambiguous-signal

When declared configuration is insufficient to confirm a weakness, the skill SHALL record
the result as inconclusive rather than emitting a Finding.

---

# Evidence On Error

The skill SHALL record Evidence for suppressed, deferred, partial, and inconclusive outcomes
to preserve auditability. Sensitive values SHALL be redacted.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
