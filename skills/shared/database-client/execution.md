# Database Client Execution Model

**File:** `skills/shared/database-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Database Client Shared Skill.

The execution model describes how the shared skill executes an operation from
connection establishment through parameterized statement execution and
transaction resolution.

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

Establish Connection (TCP Client)

↓

Encrypt Transport (TLS Client)

↓

Authenticate

↓

Begin Transaction (if requested)

↓

Execute Parameterized Statement(s)

↓

Handle Bounded Results

↓

Commit / Rollback

↓

Close Connection

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Database Client SHALL resolve security, execution gating, bounds, and
governance using the precedence defined in [configuration.md](configuration.md).

A required-encryption setting and parameterization SHALL always be enforced.

---

# Stage 2 — Rate Permit

The Database Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the operation.

---

# Stage 3 — Connection

The Database Client SHALL establish the connection through the
[TCP Client](../tcp-client/README.md), routed through the
[Proxy](../proxy/README.md) shared skill where configured.

---

# Stage 4 — Transport Encryption

Where `tls_mode` is `preferred` or `required` and the engine supports it, the
Database Client SHALL encrypt transport through the
[TLS Client](../tls-client/README.md).

Where `tls_mode` is `required` and encryption is unavailable, the operation SHALL
fail with `encryption_required_unavailable` rather than proceed in cleartext.

---

# Stage 5 — Authentication

Where authentication is configured, the Database Client SHALL authenticate
through the [Authentication](../authentication/README.md) package.

Authentication over cleartext SHALL be refused when confidentiality is required.

Credentials SHALL never appear in evidence or statement text.

---

# Stage 6 — Transaction

Where a transaction is requested, the Database Client SHALL begin it before
executing statements.

Read-only intent SHALL be preferred by default.

---

# Stage 7 — Parameterized Execution

The Database Client SHALL execute each statement using bound parameters supplied
separately from statement text.

The Database Client SHALL NOT interpolate parameter values into statement text.

`write` statements SHALL execute only when `allow_write_statements` is enabled;
schema changes SHALL require `allow_schema_changes`.

Each statement SHALL be bounded by `statement_timeout`.

---

# Stage 8 — Result Handling

The Database Client SHALL bound result sets by `max_rows` and `max_result_bytes`.

Large result sets SHALL be stored by reference.

The Database Client SHALL NOT interpret result contents as findings.

---

# Stage 9 — Transaction Resolution

The Database Client SHALL commit on success or roll back on failure where a
transaction is active.

A failure within a transaction SHALL trigger rollback before propagation.

---

# Stage 10 — Closure

The Database Client SHALL close the connection, releasing resources including on
error.

---

# Stage 11 — Evidence And Events

The Database Client SHOULD emit operation evidence and lifecycle events according
to configuration. Evidence SHALL exclude credentials and parameter values.

---

# Retry Behavior

Transient connection failures MAY be retried through the
[Retry](../retry/README.md) shared skill, each retry acquiring a fresh permit.

Write statements SHALL be retried only when idempotent and authorized, and SHALL
prefer transactional re-execution to avoid partial effects.

---

# Determinism

Given identical configuration and inputs, the Database Client SHALL enforce
identical bounds and produce identical outcome classifications for the same
observed engine behavior.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed operation SHALL roll back any active transaction and SHALL NOT leak
partial state.

---

# Execution Outputs

The execution model SHALL produce

- Statement results with bounded result references
- Transaction outcomes
- Operation metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [TCP Client](../tcp-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Execution Model](../../core/execution-model.md)
