# Parameter Mining Error Model

**File:** `skills/active-testing/parameter-mining/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Parameter Mining Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target outside Scope | rejected |
| policy-denied | Policy Engine denied the request | suppressed |
| approval-required | Request requires approval | awaiting_approval |
| candidate-unavailable | Candidate source did not resolve | partial |
| throttled | Rate ceiling reached | retry-or-partial |
| transport-error | HTTP Client could not complete a request | retry-or-partial |
| unreachable-target | Target did not respond | inconclusive |

---

# out-of-scope

When `target` is outside [Scope](../../../schemas/scope.md), the capability SHALL reject the
request before any probe.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) denies a request, the capability
SHALL suppress it and record the decision.

---

# approval-required

When the decision is `requires_approval`, the capability SHALL defer probing to an
`awaiting_approval` state.

---

# candidate-unavailable

When the candidate source cannot be resolved, the capability SHALL produce a partial result.

---

# throttled

When a rate ceiling is reached, the capability MAY retry within limits; persistent throttling
SHALL yield a partial result.

---

# transport-error

When the [HTTP Client](../../shared/http-client/README.md) cannot complete a request, the
capability MAY retry; persistent failure SHALL yield a partial result.

---

# unreachable-target

When the target does not respond, probing SHALL be inconclusive.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
