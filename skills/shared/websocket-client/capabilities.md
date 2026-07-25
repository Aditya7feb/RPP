# WebSocket Client Capabilities

**File:** `skills/shared/websocket-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the WebSocket Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[WebSocket Client Interface](interface.md).

---

# Capability Model

```
Handshake

Secure Channel

Frame Exchange

Negotiation

Lifecycle

Governance

Observability
```

---

# Handshake Capabilities

## Upgrade Handshake

The WebSocket Client SHALL perform the upgrade handshake through the
[HTTP Client](../http-client/README.md).

---

## Handshake Evidence

The WebSocket Client SHALL preserve the handshake as an
[HTTP Transaction](../../../schemas/http-transaction.md).

---

# Secure Channel Capabilities

## Secure Connection

The WebSocket Client SHALL establish `wss` connections through the
[TLS Client](../tls-client/README.md).

---

# Frame Exchange Capabilities

## Text And Binary Frames

The WebSocket Client SHALL exchange bounded text and binary frames.

---

## Control Frames

The WebSocket Client SHALL manage ping, pong, and close frames and SHALL respond
to ping with pong.

---

## Fragmentation

The WebSocket Client SHALL handle fragmented messages within configured bounds.

---

# Negotiation Capabilities

## Subprotocol Negotiation

The WebSocket Client SHALL negotiate subprotocols declaratively.

---

## Extension Negotiation

The WebSocket Client SHALL negotiate extensions declaratively.

---

# Lifecycle Capabilities

## Lifetime Bounding

The WebSocket Client SHALL enforce a maximum connection lifetime.

---

## Graceful Close

The WebSocket Client SHALL perform a graceful close with a code and reason.

---

# Governance Capabilities

## Rate And Proxy Governance

The WebSocket Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The WebSocket Client MAY retry transient handshake failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The WebSocket Client SHOULD capture WebSocket evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The WebSocket Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The WebSocket Client SHOULD expose metrics including frames sent, frames
received, bytes exchanged, and connection duration.

---

# Capability Boundaries

The WebSocket Client SHALL NOT

- Interpret message semantics
- Produce findings
- Authenticate independently
- Persist secret payloads

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Upgrade Handshake | Handshake | SHALL |
| Handshake Evidence | Handshake | SHALL |
| Secure Connection | Secure Channel | SHALL |
| Text And Binary Frames | Frame Exchange | SHALL |
| Control Frames | Frame Exchange | SHALL |
| Fragmentation | Frame Exchange | SHALL |
| Subprotocol Negotiation | Negotiation | SHALL |
| Extension Negotiation | Negotiation | SHALL |
| Lifetime Bounding | Lifecycle | SHALL |
| Graceful Close | Lifecycle | SHALL |
| Rate And Proxy Governance | Governance | SHALL |
| Retry Governance | Governance | MAY |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [HTTP Client](../http-client/README.md)
