# Fuzzing Error Model

**File:** `skills/active-testing/fuzzing/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Fuzzing Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target outside Scope | rejected |
| policy-denied | Policy Engine denied a delivery | suppressed |
| approval-required | Delivery or payload requires approval | awaiting_approval |
| corpus-unavailable | Corpus could not be resolved | partial |
| throttled | Rate ceiling reached | retry-or-partial |
| transport-error | HTTP Client could not complete a delivery | retry-or-partial |
| unreachable-target | Target did not respond | inconclusive |

---

# out-of-scope

When `target` is outside [Scope](../../../schemas/scope.md), the capability SHALL reject the
request before any delivery.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) denies a delivery, the capability
SHALL suppress it and, where configured, halt further delivery.

---

# approval-required

When the decision is `requires_approval`, including for a payload marked `requires_approval`,
the capability SHALL defer delivery to an `awaiting_approval` state.

---

# corpus-unavailable

When the corpus cannot be resolved, the capability SHALL produce a partial result.

---

# throttled

When a rate ceiling is reached, the capability MAY pause within limits; persistent throttling
SHALL yield a partial result.

---

# transport-error

When the [HTTP Client](../../shared/http-client/README.md) cannot complete a delivery, the
capability MAY retry; persistent failure SHALL yield a partial result.

---

# unreachable-target

When the target does not respond, delivery SHALL be inconclusive.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
