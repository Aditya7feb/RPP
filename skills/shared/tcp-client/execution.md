# TCP Client Execution Model

**File:** `skills/shared/tcp-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the TCP Client Shared Skill.

The execution model describes how the shared skill processes a connection
request from endpoint resolution through establishment, byte exchange, and
closure.

The model is deterministic given the same configuration, resolution, and inputs.

---

# Execution Overview

```
Receive Connect Request

↓

Resolve Configuration

↓

Resolve Endpoint

↓

Acquire Rate Permit

↓

Route Through Proxy (if configured)

↓

Establish Connection (bounded)

↓

Exchange Bytes (bounded)

↓

Close Connection

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The TCP Client SHALL resolve timeouts, bounds, and governance policies using the
precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Endpoint Resolution

Where a hostname is supplied, the TCP Client SHALL resolve it through the
[DNS Client](../dns-client/README.md), optionally reusing results through the
[Cache](../cache/README.md).

Where an address is supplied, the TCP Client SHALL use it directly.

---

# Stage 3 — Rate Permit

The TCP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the connection attempt.

Each retry attempt SHALL acquire its own permit.

---

# Stage 4 — Proxy Routing

Where a [Proxy Configuration](../../../schemas/proxy-configuration.md) applies,
the TCP Client SHALL establish the connection through the
[Proxy](../proxy/README.md) shared skill, honoring bypass and governance rules.

---

# Stage 5 — Connection Establishment

The TCP Client SHALL establish a connection bounded by the `connect` timeout.

A failure to connect within the bound SHALL produce a canonical timeout or
connection error per [error-model.md](error-model.md).

Transient failures MAY be retried through the [Retry](../retry/README.md) shared
skill.

---

# Stage 6 — Byte Exchange

The TCP Client SHALL write the caller's `send` bytes bounded by the `write`
timeout and read according to the `expect` strategy bounded by the `read`
timeout and `max_bytes`.

The TCP Client SHALL NOT interpret payload contents.

Reads SHALL never exceed `max_bytes`; a breach SHALL truncate and produce a
bounded result flagged accordingly.

---

# Stage 7 — Closure

The TCP Client SHALL close the connection, supporting half-close where the caller
requested it.

Closure SHALL release all associated resources, including on error.

---

# Stage 8 — Evidence And Events

The TCP Client SHOULD emit connection evidence and lifecycle events according to
configuration. Evidence SHALL exclude secret payloads.

---

# Determinism

Given identical configuration, resolution, and inputs, the TCP Client SHALL
produce identical outcomes apart from timing.

---

# Concurrency

The TCP Client SHALL support concurrent connections bounded by `max_concurrent`.

Connections beyond the bound SHALL wait or be rejected according to rate
governance.

---

# Deadlines

No stage SHALL extend beyond the supplied `deadline`.

An operation exceeding its deadline SHALL produce a `timed_out` outcome.

---

# Interaction With Higher-Level Clients

Higher-level clients such as the [TLS Client](../tls-client/README.md) and
the SMTP Client SHALL layer their protocols atop the byte
stream provided by the TCP Client without re-implementing transport.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed connection SHALL be fully torn down and SHALL NOT leak partial transport
state to the caller.

---

# Execution Outputs

The execution model SHALL produce

- A bounded connection result
- Connection timing
- Transport metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Proxy](../proxy/README.md)
- [Execution Model](../../core/execution-model.md)
