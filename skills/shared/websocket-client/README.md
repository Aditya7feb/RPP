# WebSocket Client Shared Skill

**File:** `skills/shared/websocket-client/README.md`

**Version:** 1.0.0

---

# Purpose

The WebSocket Client Shared Skill provides the canonical,
implementation-independent mechanism for establishing and exchanging messages
over WebSocket connections within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to negotiate WebSocket upgrades and frame
messages directly, this shared skill centralizes the upgrade handshake, frame
exchange, subprotocol negotiation, connection lifecycle, governance, and
observability.

All packages that require WebSocket transport SHALL delegate to this shared
skill.

---

# Goals

The WebSocket Client Shared Skill SHALL

- Abstract WebSocket transport behind a stable interface
- Perform the upgrade handshake through the [HTTP Client](../http-client/README.md)
- Secure `wss` connections through the [TLS Client](../tls-client/README.md)
- Exchange text and binary frames with bounded sizes
- Negotiate subprotocols and extensions declaratively
- Pace and route through the shared governance skills
- Produce WebSocket evidence
- Integrate with platform observability

---

# Non-Goals

The WebSocket Client Shared Skill SHALL NOT

- Interpret application-layer message semantics
- Detect vulnerabilities
- Produce security findings
- Perform authentication independently
- Parse or interpret message payloads as findings

The WebSocket Client moves frames. Application and security interpretation belong
to domain skills such as an API-security WebSocket skill.

---

# Design Principles

The WebSocket Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Layered atop existing HTTP and TLS shared skills
- Bounded in message size and connection lifetime
- Governed
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

WebSocket Client Shared Skill

├── Upgrade Coordinator      → HTTP Client
├── Secure Channel           → TLS Client
├── Frame Exchanger
├── Subprotocol Negotiator
├── Lifecycle Manager
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The WebSocket Client establishes and drives a connection but SHALL remain
unaware of the transport adapter implementation.

---

# Responsibilities

The WebSocket Client Shared Skill is responsible for

- Performing the upgrade handshake via the
  [HTTP Client](../http-client/README.md), preserving the resulting
  [HTTP Transaction](../../../schemas/http-transaction.md) as evidence
- Securing `wss` connections via the [TLS Client](../tls-client/README.md)
- Negotiating subprotocols and extensions
- Exchanging bounded text and binary frames
- Managing ping, pong, and close frames
- Applying rate, retry, and proxy governance
- Emitting WebSocket lifecycle events and capturing evidence

---

# Connection Lifecycle

```
Receive Connect Request

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

Handle Ping / Pong / Close

↓

Close Connection

↓

Emit Evidence and Events
```

The handshake and close outcomes SHOULD be preserved as evidence.

---

# Upgrade Handshake

The WebSocket Client SHALL perform the upgrade through the
[HTTP Client](../http-client/README.md), which applies existing header, cookie,
authentication, and redirect handling.

The resulting handshake SHALL be preserved as an
[HTTP Transaction](../../../schemas/http-transaction.md) for evidence.

A failed or rejected upgrade SHALL produce a canonical error.

---

# Secure Connections

For `wss`, the WebSocket Client SHALL establish the secure channel through the
[TLS Client](../tls-client/README.md), inheriting its validation and
interception awareness.

Certificate validation outcomes SHALL be reported as data, not findings.

---

# Frame Exchange

The WebSocket Client SHALL exchange text and binary frames bounded by configured
message and fragment sizes.

The WebSocket Client SHALL manage control frames, including ping, pong, and
close, and SHALL respond to ping with pong.

The WebSocket Client SHALL NOT interpret payload contents.

---

# Subprotocols And Extensions

The WebSocket Client SHALL negotiate subprotocols and extensions declaratively
from the connection request.

Unsupported requested subprotocols SHALL result in a negotiated outcome, not an
error, unless the caller requires a specific subprotocol.

---

# Governance

The WebSocket Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) for the
  connection and MAY pace outbound frames
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover transient handshake failures through the [Retry](../retry/README.md)
  shared skill

Long-lived connections SHALL respect a configured maximum lifetime.

---

# Evidence

The WebSocket Client Shared Skill SHOULD capture

- Handshake transaction
- Negotiated subprotocol and extensions
- Frame counts and sizes
- Close code and reason
- Connection duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads.

---

# Events

The WebSocket Client Shared Skill SHOULD publish

- HandshakeStarted
- HandshakeCompleted
- SubprotocolNegotiated
- FrameSent
- FrameReceived
- ConnectionClosed
- ConnectionFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The WebSocket Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Proxy](../proxy/README.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [HTTP Transaction Schema](../../../schemas/http-transaction.md)

The WebSocket Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- API-security WebSocket skills
- Real-time application testing skills

---

# Outputs

Typical outputs MAY include

- A handshake transaction
- A bounded frame-exchange result
- Connection metrics
- WebSocket evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The WebSocket Client Shared Skill SHALL

- Bound message sizes to prevent memory exhaustion
- Bound connection lifetime to prevent resource leakage
- Respect Rules of Engagement through rate and proxy governance
- Protect secret payloads from evidence and logs
- Preserve auditability

Unbounded frames or connections can exhaust resources. The shared skill SHALL
enforce bounds.

---

# Best Practices

Consumers SHOULD

- Bound message sizes and connection lifetime
- Require specific subprotocols only when necessary
- Reference shared rate, retry, and proxy policies
- Capture handshake and close evidence
- Delegate message semantics to domain skills

---

# Anti-Patterns

Consumers SHOULD NOT

- Negotiate upgrades directly
- Frame messages manually
- Interpret payloads as findings within the transport layer
- Leave connections open without a lifetime bound
- Persist secret payloads in evidence

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-websocket-transport-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Proxy](../proxy/README.md)
- [Rate Limiter](../rate-limiter/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)
- [TLS Session](../../../schemas/tls-session.md)

---

# Architecture Decisions

- [ADR-001 — WebSocket Transport Abstraction](adr/ADR-001-websocket-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Permessage-deflate negotiation detail
- Multiplexed subprotocol channels
- Streaming frame notifications
- Backpressure-aware flow control

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant WebSocket Client Shared Skill provides a bounded, governed, and
implementation-independent WebSocket transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable frame exchange atop the existing HTTP and TLS
shared skills, without embedding application semantics or transport
implementations in consumers.
