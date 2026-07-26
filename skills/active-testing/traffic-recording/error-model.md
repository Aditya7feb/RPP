# Traffic Recording Error Model

**File:** `skills/active-testing/traffic-recording/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Traffic Recording Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Selected traffic outside Scope | rejected |
| policy-denied | Policy Engine denied recording | suppressed |
| approval-required | Recording requires approval | awaiting_approval |
| bounds-exhausted | Capture bounds reached | partial |
| storage-error | Artifact could not be written | partial |

---

# out-of-scope

When selected exchanges are outside [Scope](../../../schemas/scope.md), the capability SHALL
exclude them and, where all selection is out of scope, reject the request.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) denies recording, the capability
SHALL suppress it and record the decision.

---

# approval-required

When the decision is `requires_approval`, the capability SHALL defer recording to an
`awaiting_approval` state.

---

# bounds-exhausted

When capture bounds are reached, the capability SHALL finalize a partial recording.

---

# storage-error

When an Artifact cannot be written, the capability SHALL return a partial result.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
