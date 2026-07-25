# Secrets Client Execution Model

**File:** `skills/shared/secrets-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Secrets Client Shared Skill.

The execution model describes how the shared skill resolves a secret reference and
either returns an opaque handle or brokers application, never exposing the value.

The model is deterministic given the same configuration, reference, and store
state.

---

# Execution Overview

```
Receive Secret Request

↓

Resolve Configuration

↓

Resolve Reference To Store

↓

Retrieve Within Boundary (value never leaves)

↓

Mode?

├── resolve_handle → Issue Opaque Handle

└── broker_apply   → Apply To Broker Target

↓

Track Lease / Rotation

↓

Emit Non-Sensitive Evidence

↓

Return Result (never a value)
```

---

# Stage 1 — Configuration Resolution

The Secrets Client SHALL resolve stores, handle lifetime, and redaction using the
precedence defined in [configuration.md](configuration.md).

Redaction and non-return of values SHALL always be enforced.

---

# Stage 2 — Reference Resolution

The Secrets Client SHALL resolve the `secret_ref` to a configured store and
namespace.

An unresolved reference SHALL produce a `not_found` outcome.

---

# Stage 3 — Retrieval Within Boundary

The Secrets Client SHALL retrieve the secret within the secrets boundary.

The value SHALL NOT cross the interface to general consumers and SHALL NOT be
logged or persisted.

---

# Stage 4 — Mode Handling

```
resolve_handle → issue an opaque handle that identifies but does not encode the
                 value

broker_apply   → apply the value to the declared broker target through the
                 Authentication broker without returning it
```

Brokered application SHALL redact the value from all evidence and results.

---

# Stage 5 — Lease And Rotation

The Secrets Client SHALL record lease and version information where supported.

Leases approaching expiry SHALL be renewed per configuration; expired leases
SHALL invalidate handles.

Where rotation is detected, handles SHALL reflect the current version.

---

# Stage 6 — Retention And Clearing

Any in-memory retention SHALL be bounded by `max_lifetime` and cleared on lease
expiry when `clear_on_expiry` is `true`.

Secret values SHALL NOT be cached in a persistable form.

---

# Stage 7 — Evidence And Events

The Secrets Client SHOULD emit non-sensitive access evidence and lifecycle events
according to configuration.

Evidence and events SHALL NEVER contain secret values.

---

# Determinism

Given identical configuration, reference, and store state, the Secrets Client
SHALL produce identical outcomes apart from lease and rotation timing.

---

# Concurrency

The Secrets Client SHALL support concurrent resolutions.

Concurrent brokered applications SHALL NOT expose values across contexts.

---

# Interaction With Other Shared Skills

- The [Authentication](../authentication/README.md) package is the broker that
  applies resolved secrets at the point of use.
- The [Logging](../logging/README.md) shared package SHALL redact any
  incidental secret material, providing defense in depth.
- The [Cache](../cache/README.md) shared skill SHALL NOT store secret values.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failure SHALL NEVER expose a secret value, including in error context.

---

# Execution Outputs

The execution model SHALL produce

- Opaque handles or brokered-application confirmations
- Lease and version identifiers
- Non-sensitive access evidence references

Outputs SHALL NEVER include secret values.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
- [Execution Model](../../core/execution-model.md)
