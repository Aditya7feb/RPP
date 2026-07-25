# TCP Client Shared Skill

**File:** `skills/shared/tcp-client/README.md`

**Version:** 1.0.0

---

# Purpose

The TCP Client Shared Skill provides the canonical, implementation-independent
mechanism for establishing and exchanging data over Transmission Control
Protocol (TCP) connections within the Robust PenTest Platform (RPP).

Rather than allowing individual skills and higher-level clients to open raw
sockets directly, this shared skill centralizes connection establishment, byte
exchange, timeout handling, proxy routing, rate governance, and connection
observability.

All packages that require raw TCP transport SHALL delegate to this shared skill.

---

# Goals

The TCP Client Shared Skill SHALL

- Abstract TCP transport behind a stable interface
- Establish connections to a host and port
- Exchange byte streams with bounded timeouts
- Route connections through the [Proxy](../proxy/README.md) shared skill
- Pace connections through the [Rate Limiter](../rate-limiter/README.md)
- Recover from transient failures through the [Retry](../retry/README.md) skill
- Produce connection evidence
- Integrate with platform observability

---

# Non-Goals

The TCP Client Shared Skill SHALL NOT

- Interpret application-layer protocols
- Perform TLS negotiation
- Detect vulnerabilities
- Produce security findings
- Enumerate ports or targets
- Parse or interpret exchanged payloads

The TCP Client moves bytes reliably. Application semantics belong to
higher-level clients such as the [TLS Client](../tls-client/README.md),
the SMTP Client, and
[HTTP Client](../http-client/README.md). Port enumeration belongs to discovery
skills.

---

# Design Principles

The TCP Client Shared Skill SHALL be

- Deterministic given the same configuration and inputs
- Transport focused
- Bounded in time and resource use
- Proxy aware
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Higher-Level Client or Domain Skill

↓

TCP Client Shared Skill

├── Endpoint Resolver
├── Connection Establisher
├── Stream Exchanger
├── Timeout Guard
├── Proxy Coordinator
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The TCP Client establishes a connection and exchanges bytes but SHALL remain
unaware of the transport adapter implementation.

---

# Responsibilities

The TCP Client Shared Skill is responsible for

- Resolving the destination endpoint through the
  [DNS Client](../dns-client/README.md) where a hostname is supplied
- Establishing a bounded TCP connection
- Routing through the [Proxy](../proxy/README.md) shared skill where configured
- Applying [Rate Limit](../../../schemas/rate-limit-policy.md) and
  [Retry](../../../schemas/retry-policy.md) policies
- Exchanging byte streams with bounded read and write timeouts
- Emitting connection lifecycle events
- Capturing connection evidence

---

# Connection Lifecycle

```
Receive Connect Request

↓

Resolve Endpoint

↓

Acquire Rate Permit

↓

Route Through Proxy (if configured)

↓

Establish Connection (bounded)

↓

Exchange Bytes (bounded read/write)

↓

Close Connection

↓

Emit Evidence and Events
```

The connection outcome SHOULD be preserved as evidence.

---

# Endpoint Resolution

Where a hostname is supplied, the TCP Client SHALL resolve it through the
[DNS Client](../dns-client/README.md).

Where an address is supplied, the TCP Client SHALL use it directly.

Resolution results MAY be reused through the [Cache](../cache/README.md) shared
skill.

---

# Timeouts

The TCP Client SHALL enforce bounded

- connection timeouts
- read timeouts
- write timeouts
- total operation deadlines

No operation SHALL block indefinitely. A breached bound SHALL produce a canonical
timeout error.

---

# Proxy Routing

Where a [Proxy Configuration](../../../schemas/proxy-configuration.md) applies,
the TCP Client SHALL establish the connection through the
[Proxy](../proxy/README.md) shared skill, honoring bypass and governance rules.

---

# Rate And Retry

The TCP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for each connection attempt, including
retries, and MAY recover transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Evidence

The TCP Client Shared Skill SHOULD capture

- Endpoint
- Connection outcome
- Timing (connect, first byte, close)
- Bytes sent and received
- Proxy routing decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payload material.

---

# Events

The TCP Client Shared Skill SHOULD publish

- ConnectionRequested
- EndpointResolved
- ConnectionEstablished
- BytesExchanged
- ConnectionClosed
- ConnectionFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The TCP Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [DNS Client](../dns-client/README.md)
- [Proxy](../proxy/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The TCP Client Shared Skill SHALL NOT depend on domain skills or higher-level
clients.

---

# Consumers

Typical consumers include

- [TLS Client](../tls-client/README.md)
- SMTP Client
- FTP Client
- SSH Client
- Database Client
- Port discovery skills

---

# Outputs

Typical outputs MAY include

- A bounded byte-exchange result
- Connection timing
- Connection evidence references
- Transport metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The TCP Client Shared Skill SHALL

- Enforce bounded connections to prevent resource exhaustion
- Respect Rules of Engagement through rate and proxy governance
- Route only to authorized endpoints
- Protect secret payloads from evidence and logs
- Preserve auditability

Unbounded or unauthorized connections can harm targets or violate scope. The
shared skill SHALL enforce bounds and governance.

---

# Best Practices

Consumers SHOULD

- Supply explicit timeouts
- Reference shared rate, retry, and proxy policies
- Reuse resolution through the cache where appropriate
- Capture connection evidence
- Delegate application semantics to higher-level clients

---

# Anti-Patterns

Consumers SHOULD NOT

- Open raw sockets directly
- Perform unbounded reads or writes
- Interpret application protocols in the TCP layer
- Bypass proxy or rate governance
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
- adr/ADR-001-tcp-transport-abstraction.md

---

# Related Shared Packages

- [TLS Client](../tls-client/README.md)
- [Proxy](../proxy/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [DNS Client](../dns-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [Proxy Configuration](../../../schemas/proxy-configuration.md)
- [Rate Limit Policy](../../../schemas/rate-limit-policy.md)
- [Retry Policy](../../../schemas/retry-policy.md)

---

# Architecture Decisions

- [ADR-001 — TCP Transport Abstraction](adr/ADR-001-tcp-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Connection pooling and keep-alive reuse
- Happy-eyeballs dual-stack connection racing
- Bandwidth shaping
- Raw socket options expressed as canonical descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TCP Client Shared Skill provides a bounded, governed, and
implementation-independent TCP transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable byte exchange across every higher-level client
while enforcing timeouts and governance, without embedding application semantics
or transport implementations in consumers.
