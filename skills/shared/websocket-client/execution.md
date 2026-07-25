# WebSocket Client Execution Model

**File:** `skills/shared/websocket-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the WebSocket Client Shared Skill.

The execution model describes how the shared skill processes a connection request
from the upgrade handshake through frame exchange and closure.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Connect Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Perform Upgrade Handshake (HTTP Client)

↓

Secure Channel (TLS Client, for wss)

↓

Negotiate Subprotocol

↓

Exchange Frames (bounded)

↓

Handle Control Frames

↓

Close Connection

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The WebSocket Client SHALL resolve bounds, negotiation, and governance using the
precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Rate Permit

The WebSocket Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the connection.

---

# Stage 3 — Upgrade Handshake

The WebSocket Client SHALL perform the upgrade through the
[HTTP Client](../http-client/README.md), which applies header, cookie,
authentication, redirect, and proxy handling.

The handshake SHALL be preserved as an
[HTTP Transaction](../../../schemas/http-transaction.md).

A rejected upgrade SHALL produce a canonical handshake error, retryable through
the [Retry](../retry/README.md) shared skill where transient.

---

# Stage 4 — Secure Channel

For `wss`, the WebSocket Client SHALL establish the secure channel through the
[TLS Client](../tls-client/README.md), inheriting validation and interception
awareness.

---

# Stage 5 — Subprotocol Negotiation

The WebSocket Client SHALL negotiate a subprotocol from the caller preference
list.

When `require_subprotocol` is `true` and no acceptable subprotocol is offered,
the connection SHALL be closed and a canonical error produced.

---

# Stage 6 — Frame Exchange

The WebSocket Client SHALL send and receive text and binary frames bounded by
`max_message_bytes` and `max_fragment_bytes`.

Messages exceeding bounds SHALL be rejected rather than buffered without limit.

The WebSocket Client SHALL NOT interpret payload contents.

---

# Stage 7 — Control Frames

The WebSocket Client SHALL respond to ping with pong and SHALL honor peer close
frames.

Idle connections exceeding `idle_timeout` SHALL be closed.

---

# Stage 8 — Closure

The WebSocket Client SHALL perform a graceful close with a code and reason and
SHALL release all resources.

Connections exceeding `max_connection_lifetime` SHALL be closed.

---

# Stage 9 — Evidence And Events

The WebSocket Client SHOULD emit handshake and close evidence and lifecycle
events according to configuration. Evidence SHALL exclude secret payloads.

---

# Determinism

Given identical configuration and inputs, the WebSocket Client SHALL enforce
identical bounds and produce identical outcome classifications for the same
observed peer behavior.

---

# Concurrency

The WebSocket Client SHALL support concurrent connections subject to rate
governance.

Frame ordering within a single connection SHALL be preserved.

---

# Interaction With Other Shared Skills

- The [HTTP Client](../http-client/README.md) performs the handshake.
- The [TLS Client](../tls-client/README.md) secures `wss` channels.
- The [Rate Limiter](../rate-limiter/README.md), [Retry](../retry/README.md),
  and [Proxy](../proxy/README.md) shared skills govern the connection.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed connection SHALL be fully closed and SHALL NOT leak partial state.

---

# Execution Outputs

The execution model SHALL produce

- A handshake transaction reference
- A bounded frame-exchange result
- Connection metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Execution Model](../../core/execution-model.md)
