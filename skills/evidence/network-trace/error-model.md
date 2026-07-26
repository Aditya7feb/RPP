# Network Trace Error Model

**File:** `skills/evidence/network-trace/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Network Trace Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target outside Scope | rejected |
| policy-denied | Policy Engine denied the capture | suppressed |
| approval-required | Capture requires approval | awaiting_approval |
| capture-error | Transport client could not capture flows | retry-or-partial |
| bounds-exhausted | Capture bounds reached | partial |
| promotion-error | Shared Evidence lifecycle could not promote the trace | partial |

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

# capture-error

When the [TCP Client](../../shared/tcp-client/README.md) or
[UDP Client](../../shared/udp-client/README.md) cannot capture flows, the capability MAY retry
within limits; persistent failure SHALL yield a partial result.

---

# bounds-exhausted

When capture bounds are reached, the capability SHALL finalize a partial trace.

---

# promotion-error

When the shared [Evidence](../../shared/evidence/README.md) lifecycle cannot promote the trace, the
capability SHALL return a partial result retaining the Artifact reference.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
