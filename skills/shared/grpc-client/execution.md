# gRPC Client Execution Model

**File:** `skills/shared/grpc-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the gRPC Client Shared Skill.

The execution model describes how the shared skill processes a call from channel
establishment through message exchange and status mapping.

The model is deterministic in bounds given the same configuration and inputs.

---

# Execution Overview

```
Receive Invoke Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Establish HTTP/2 Channel (HTTP Client)

↓

Secure Channel (TLS Client)

↓

Send Request Message(s)

↓

Receive Response Message(s) (bounded)

↓

Map Status And Trailers

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The gRPC Client SHALL resolve bounds and governance using the precedence defined
in [configuration.md](configuration.md).

---

# Stage 2 — Rate Permit

The gRPC Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for the call.

Each retry attempt SHALL acquire its own permit.

---

# Stage 3 — Channel Establishment

The gRPC Client SHALL establish an HTTP/2 channel through the
[HTTP Client](../http-client/README.md), routed through the
[Proxy](../proxy/README.md) shared skill where configured.

---

# Stage 4 — Secure Channel

The gRPC Client SHALL secure the channel through the
[TLS Client](../tls-client/README.md), inheriting validation and interception
awareness.

---

# Stage 5 — Request Messages

The gRPC Client SHALL send request messages according to the method `kind`,
carrying request metadata.

Client-streaming and bidirectional calls SHALL bound sent message counts and
sizes.

The gRPC Client SHALL NOT interpret message contents.

---

# Stage 6 — Response Messages

The gRPC Client SHALL receive response messages bounded by `max_messages` and
`max_message_bytes`.

Server-streaming and bidirectional calls SHALL stop receiving when bounds or the
`deadline` are reached.

---

# Stage 7 — Status Mapping

The gRPC Client SHALL read the trailing gRPC status and map it to a canonical
outcome.

- `OK` maps to `completed`
- Configured retryable statuses map to retryable errors
- Other non-`OK` statuses map to non-retryable `status_error`

Status interpretation as a security weakness SHALL remain with domain skills.

---

# Stage 8 — Evidence And Events

The gRPC Client SHOULD emit call evidence and lifecycle events according to
configuration. Evidence SHALL exclude secret payloads and metadata.

---

# Retry Behavior

Retryable statuses MAY be retried through the [Retry](../retry/README.md) shared
skill, subject to idempotency, with each retry acquiring a fresh permit.

Non-idempotent calls SHALL NOT be retried unless declared safe.

---

# Determinism

Given identical configuration and inputs, the gRPC Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed server
behavior.

---

# Concurrency

The gRPC Client SHALL support concurrent calls subject to rate governance.

Message ordering within a single stream SHALL be preserved.

---

# Interaction With Other Shared Skills

- The [HTTP Client](../http-client/README.md) provides the HTTP/2 channel.
- The [TLS Client](../tls-client/README.md) secures the channel.
- The [Rate Limiter](../rate-limiter/README.md), [Retry](../retry/README.md),
  and [Proxy](../proxy/README.md) shared skills govern the call.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failed call SHALL be fully torn down and SHALL NOT leak partial state.

---

# Execution Outputs

The execution model SHALL produce

- A bounded call result
- gRPC status and trailers
- Call metrics
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
