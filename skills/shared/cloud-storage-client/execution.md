# Cloud Storage Client Execution Model

**File:** `skills/shared/cloud-storage-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Cloud Storage Client Shared
Skill.

The execution model describes how the shared skill performs an object operation
from scope confinement through encryption enforcement, the operation itself, and
access-metadata observation.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Operation Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Confine To Authorized Scope

↓

Authenticate

↓

Enforce Encryption (for writes)

↓

Perform Operation (bounded, authorized)

↓

Observe Access Metadata

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Cloud Storage Client SHALL resolve scopes, encryption, execution gating, and
bounds using the precedence defined in [configuration.md](configuration.md).

Scope confinement and required encryption SHALL always be enforced.

---

# Stage 2 — Rate Permit

The Cloud Storage Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the operation.

---

# Stage 3 — Scope Confinement

The Cloud Storage Client SHALL confine the operation to an authorized scope.

An object key outside the scope bucket and prefix SHALL be rejected with
`scope_rejected`.

---

# Stage 4 — Authentication

The Cloud Storage Client SHALL authenticate through the
[Authentication](../authentication/README.md) package.

Client-side keys, where used, SHALL be resolved through the
[Secrets Client](../secrets-client/README.md) without exposure.

---

# Stage 5 — Encryption Enforcement

For writes, where `require_server_side` is `true` and encryption is unavailable,
the operation SHALL fail with `encryption_required_unavailable` rather than store
unencrypted data.

---

# Stage 6 — Operation

The Cloud Storage Client SHALL perform the operation bounded by configured
limits.

- `list` SHALL bound keys by `max_list_keys`
- `read` SHALL bound bytes by `max_object_bytes` and store content by reference
- `write` SHALL bound bytes and require encryption and a writable scope
- `stat` SHALL return object metadata
- `delete` SHALL require authorization
- `presign` SHALL generate a bounded-lifetime reference where permitted

---

# Stage 7 — Access-Metadata Observation

The Cloud Storage Client SHALL observe access metadata such as public-access
flags and encryption status and SHALL report it as data.

The client SHALL NOT classify metadata as a misconfiguration.

---

# Stage 8 — Evidence And Events

The Cloud Storage Client SHOULD emit operation evidence and lifecycle events
according to configuration. Evidence SHALL exclude object contents and presigned
references.

---

# Retry Behavior

Transient provider failures MAY be retried through the [Retry](../retry/README.md)
shared skill, each retry acquiring a fresh permit.

Write and delete operations SHALL be retried only when idempotent and authorized.

---

# Determinism

Given identical configuration and inputs, the Cloud Storage Client SHALL enforce
identical confinement and bounds and produce identical outcome classifications
for the same observed provider state.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A scope violation SHALL never perform the operation.

A failed write SHALL NOT leave a partially stored object where the provider
supports atomic completion.

---

# Execution Outputs

The execution model SHALL produce

- Object listings
- Object contents by reference
- Access metadata
- Operation metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Secrets Client](../secrets-client/README.md)
- [Execution Model](../../core/execution-model.md)
