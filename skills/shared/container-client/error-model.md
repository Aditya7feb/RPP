# Container Client Error Model

**File:** `skills/shared/container-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Container Client Shared Skill and
their mapping to outcomes. Errors are deterministic and implementation independent.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Engine, image, or container outside authorized scope | rejected |
| policy-denied | Policy Engine denied a mutation | denied |
| approval-required | Mutation or workload execution requires approval | awaiting_approval |
| elevated-authorization-required | Run or exec requires elevated authorization | awaiting_approval |
| authentication-failed | Credentials could not be resolved or accepted | rejected |
| bounds-exhausted | Result or inspection bounds reached before completion | partial |
| transport-error | HTTP or Filesystem Client could not complete the request | retry-or-partial |
| unreachable-engine | Engine did not respond | inconclusive |

---

# out-of-scope

When a target is outside authorized scope, the client SHALL reject the operation before any
request.

---

# policy-denied

When the [Policy Engine](../policy-engine/README.md) denies a mutation, the client SHALL
suppress it and record the decision.

---

# approval-required

When a mutation or workload execution requires approval, the client SHALL defer it to an
`awaiting_approval` state and SHALL NOT proceed until approval is granted.

---

# elevated-authorization-required

When a run or exec operation is requested without elevated authorization, the client SHALL
defer it and SHALL NOT execute the workload.

---

# authentication-failed

When credentials cannot be resolved or are rejected, the client SHALL reject the operation
without leaking credential material.

---

# bounds-exhausted

When configured result or inspection bounds are reached, the client SHALL return a partial
result marked accordingly.

---

# transport-error

When the [HTTP Client](../http-client/README.md) or
[Filesystem Client](../filesystem-client/README.md) cannot complete a request, the client MAY
retry through the [Retry](../retry/README.md) shared skill; persistent failure SHALL yield a
partial result.

---

# unreachable-engine

When the engine does not respond, the operation SHALL be inconclusive.

---

# Evidence On Error

The client SHALL record evidence for rejected, denied, deferred, partial, and inconclusive
outcomes to preserve auditability. Credentials SHALL be redacted.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
