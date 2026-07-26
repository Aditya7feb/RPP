# HTTP Archive Error Model

**File:** `skills/evidence/http-archive/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the HTTP Archive Capability.

---

# Error Categories

| Category | Meaning | Outcome |
|----------|---------|---------|
| out-of-scope | Target outside Scope | rejected |
| policy-denied | Policy Engine denied a request | suppressed |
| approval-required | Request requires approval | awaiting_approval |
| throttled | Rate ceiling reached | retry-or-partial |
| transport-error | HTTP Client could not complete a request | retry-or-partial |
| bounds-exhausted | Archive bounds reached | partial |
| promotion-error | Shared Evidence lifecycle could not promote the archive | partial |

---

# out-of-scope

When `target` is outside [Scope](../../../schemas/scope.md), the capability SHALL reject the
request.

---

# policy-denied

When the [Policy Engine](../../shared/policy-engine/README.md) denies a request, the capability
SHALL suppress it and record the decision.

---

# approval-required

When the decision is `requires_approval`, the capability SHALL defer the request to an
`awaiting_approval` state.

---

# throttled

When a rate ceiling is reached, the capability MAY pause within limits; persistent throttling SHALL
yield a partial result.

---

# transport-error

When the [HTTP Client](../../shared/http-client/README.md) cannot complete a request, the capability
MAY retry; persistent failure SHALL yield a partial result.

---

# bounds-exhausted

When archive bounds are reached, the capability SHALL finalize a partial archive.

---

# promotion-error

When the shared [Evidence](../../shared/evidence/README.md) lifecycle cannot promote the archive,
the capability SHALL return a partial result retaining the Artifact reference.

---

# Determinism

Identical error conditions SHALL yield identical categories and outcomes.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
