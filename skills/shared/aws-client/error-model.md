# AWS Client Error Model

**File:** `skills/shared/aws-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the AWS Client Shared Skill and
their mapping to outcomes. Errors are deterministic and implementation independent.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Account, region, or service outside authorized scope | rejected |
| policy-denied | Policy Engine denied a mutation | denied |
| approval-required | Mutation requires approval | awaiting_approval |
| authentication-failed | Credentials could not be resolved or accepted | rejected |
| authorization-denied | Service denied the operation | partial |
| throttled | Rate ceiling or service throttling reached | retry-or-partial |
| pagination-exhausted | Result bounds reached before completion | partial |
| transport-error | HTTP Client could not complete the request | retry-or-partial |
| unreachable-endpoint | Service endpoint did not respond | inconclusive |

---

# out-of-scope

When a target is outside authorized scope, the client SHALL reject the operation before
any request.

---

# policy-denied

When the [Policy Engine](../policy-engine/README.md) denies a mutation, the client SHALL
suppress it and record the decision.

---

# approval-required

When a mutation requires approval, the client SHALL defer it to an `awaiting_approval`
state and SHALL NOT proceed until approval is granted.

---

# authentication-failed

When credentials cannot be resolved or are rejected, the client SHALL reject the
operation without leaking credential material.

---

# authorization-denied

When the service denies an authorized-scope operation, the client SHALL record a partial
result reflecting the denial as data.

---

# throttled

When a rate ceiling or service throttling is reached, the client MAY retry within limits;
persistent throttling SHALL yield a partial result.

---

# pagination-exhausted

When configured pagination bounds are reached, the client SHALL return a partial result
marked accordingly.

---

# transport-error

When the [HTTP Client](../http-client/README.md) cannot complete a request, the client
MAY retry through the [Retry](../retry/README.md) shared skill; persistent failure SHALL
yield a partial result.

---

# unreachable-endpoint

When a service endpoint does not respond, the operation SHALL be inconclusive.

---

# Evidence On Error

The client SHALL record evidence for rejected, denied, deferred, partial, and
inconclusive outcomes to preserve auditability. Credentials SHALL be redacted.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
