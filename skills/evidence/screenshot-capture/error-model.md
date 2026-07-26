# Screenshot Capture Error Model

**File:** `skills/evidence/screenshot-capture/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Screenshot Capture Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target outside Scope | rejected |
| policy-denied | Policy Engine denied the capture | suppressed |
| approval-required | Capture requires approval | awaiting_approval |
| render-error | Browser could not render the page | retry-or-partial |
| unreachable-target | Target did not respond | inconclusive |
| promotion-error | Shared Evidence lifecycle could not promote the capture | partial |

---

# out-of-scope

When `target` is outside [Scope](../../../schemas/scope.md), the capability SHALL reject the
capture.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) denies the capture, the capability
SHALL suppress it and record the decision.

---

# approval-required

When the decision is `requires_approval`, the capability SHALL defer the capture to an
`awaiting_approval` state.

---

# render-error

When the [Browser](../../shared/browser/README.md) cannot render the page, the capability MAY
retry within limits; persistent failure SHALL yield a partial result.

---

# unreachable-target

When the target does not respond, the capture SHALL be inconclusive.

---

# promotion-error

When the shared [Evidence](../../shared/evidence/README.md) lifecycle cannot promote the capture,
the capability SHALL return a partial result retaining the Artifact reference.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
