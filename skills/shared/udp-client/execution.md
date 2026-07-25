# UDP Client Execution Model

**File:** `skills/shared/udp-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the UDP Client Shared Skill.

The execution model describes how the shared skill processes a datagram exchange
from endpoint resolution through send, response correlation, and result
propagation.

The model is deterministic in bounds given the same configuration and inputs,
acknowledging that UDP delivery itself is unreliable.

---

# Execution Overview

```
Receive Exchange Request

↓

Resolve Configuration

↓

Resolve Endpoint

↓

Enforce Amplification Bounds

↓

Acquire Rate Permit

↓

Send Datagram

↓

Await Response Window (if expected)

↓

Correlate Response

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The UDP Client SHALL resolve windows, bounds, amplification protection, and
governance using the precedence defined in [configuration.md](configuration.md).

Amplification protection SHALL always be enforced.

---

# Stage 2 — Endpoint Resolution

Where a hostname is supplied, the UDP Client SHALL resolve it through the
[DNS Client](../dns-client/README.md).

Where an address is supplied, the UDP Client SHALL use it directly.

---

# Stage 3 — Amplification Bounds

The UDP Client SHALL reject a datagram whose payload exceeds `max_payload_bytes`
and SHALL bound response intake by `max_response_bytes` and `max_response_ratio`.

---

# Stage 4 — Rate Permit

The UDP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for each datagram sent, including
retries.

---

# Stage 5 — Send

The UDP Client SHALL send the datagram to the endpoint.

Where UDP proxying is required and unsupported, and direct egress is prohibited,
the exchange SHALL be rejected rather than sent directly.

---

# Stage 6 — Response Window

Where `expect_response` is `true`, the UDP Client SHALL await a response within
`response_window`, bounded by `deadline`.

If no response arrives, the outcome SHALL be `no_response`, which is normal and
not an error.

---

# Stage 7 — Correlation

The UDP Client SHALL correlate a received response to the originating datagram.

Datagrams received outside the window SHALL be discarded and recorded.

Response intake SHALL never exceed `max_response_bytes`.

---

# Stage 8 — Evidence And Events

The UDP Client SHOULD emit datagram evidence and lifecycle events according to
configuration. Evidence SHALL exclude secret payloads.

---

# Retry Behavior

The UDP Client SHALL retry only when the exchange is declared idempotent, using
the [Retry](../retry/README.md) shared skill, because duplicate datagrams can
cause duplicate side effects.

Each retry SHALL acquire a fresh rate permit.

---

# Determinism

Given identical configuration and inputs, the UDP Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed
delivery behavior.

UDP delivery itself remains non-deterministic and is reflected in the outcome.

---

# Concurrency

The UDP Client SHALL support concurrent exchanges bounded by `max_concurrent`.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A `no_response` outcome SHALL be distinguished from transport errors.

---

# Execution Outputs

The execution model SHALL produce

- A bounded exchange result
- Response latency where applicable
- Transport metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [DNS Client](../dns-client/README.md)
- [Execution Model](../../core/execution-model.md)
