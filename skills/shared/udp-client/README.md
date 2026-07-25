# UDP Client Shared Skill

**File:** `skills/shared/udp-client/README.md`

**Version:** 1.0.0

---

# Purpose

The UDP Client Shared Skill provides the canonical, implementation-independent
mechanism for exchanging User Datagram Protocol (UDP) datagrams within the
Robust PenTest Platform (RPP).

Rather than allowing individual skills to send datagrams directly, this shared
skill centralizes datagram exchange, response correlation, timeout handling,
rate governance, and datagram observability.

All packages that require UDP transport SHALL delegate to this shared skill.

---

# Goals

The UDP Client Shared Skill SHALL

- Abstract UDP transport behind a stable interface
- Send datagrams to a host and port
- Correlate responses within bounded windows
- Handle the connectionless, unreliable nature of UDP explicitly
- Pace datagrams through the [Rate Limiter](../rate-limiter/README.md)
- Recover through the [Retry](../retry/README.md) shared skill where safe
- Produce datagram evidence
- Integrate with platform observability

---

# Non-Goals

The UDP Client Shared Skill SHALL NOT

- Interpret application-layer protocols
- Guarantee delivery or ordering
- Detect vulnerabilities
- Produce security findings
- Enumerate ports or targets
- Parse or interpret datagram payloads

The UDP Client exchanges datagrams. Application semantics belong to higher-level
skills. Delivery guarantees are not provided by UDP and SHALL NOT be implied.

---

# Design Principles

The UDP Client Shared Skill SHALL be

- Explicit about unreliability
- Deterministic in bounds given the same configuration and inputs
- Rate governed
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill

↓

UDP Client Shared Skill

├── Endpoint Resolver
├── Datagram Sender
├── Response Correlator
├── Timeout Guard
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The UDP Client sends and correlates datagrams but SHALL remain unaware of the
transport adapter implementation.

---

# Responsibilities

The UDP Client Shared Skill is responsible for

- Resolving the destination endpoint through the
  [DNS Client](../dns-client/README.md) where a hostname is supplied
- Sending datagrams to the endpoint
- Correlating responses within a bounded response window
- Applying [Rate Limit](../../../schemas/rate-limit-policy.md) and, where safe,
  [Retry](../../../schemas/retry-policy.md) policies
- Emitting datagram lifecycle events
- Capturing datagram evidence

---

# Exchange Lifecycle

```
Receive Exchange Request

↓

Resolve Endpoint

↓

Acquire Rate Permit

↓

Send Datagram

↓

Await Response Window (bounded)

├── Response → Correlate → Return
└── No Response → Return no_response

↓

Emit Evidence and Events
```

The datagram outcome SHOULD be preserved as evidence.

---

# Unreliability Handling

The UDP Client SHALL treat the absence of a response as a normal `no_response`
outcome, not necessarily an error.

The UDP Client SHALL NOT guarantee delivery, ordering, or de-duplication.

Retries SHALL be applied only where the caller declares the exchange idempotent,
because duplicate datagrams can produce duplicate side effects.

---

# Response Correlation

Where a response is expected, the UDP Client SHALL correlate responses to the
originating datagram within a bounded response window.

Unsolicited or late datagrams outside the window SHALL be discarded and recorded.

---

# Timeouts

The UDP Client SHALL enforce a bounded response window and a total deadline.

No exchange SHALL block indefinitely awaiting a response.

---

# Rate And Retry

The UDP Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) for each datagram sent, including
retries.

Retries SHALL occur only for idempotent exchanges through the
[Retry](../retry/README.md) shared skill.

---

# Proxy Considerations

UDP proxying is supported only where the applicable
[Proxy Configuration](../../../schemas/proxy-configuration.md) and protocol
permit it, such as SOCKS5 UDP association.

Where UDP proxying is not supported and governance prohibits direct egress, the
exchange SHALL be rejected rather than sent directly.

---

# Evidence

The UDP Client Shared Skill SHOULD capture

- Endpoint
- Datagram size sent
- Response outcome and size
- Response latency
- Rate decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads.

---

# Events

The UDP Client Shared Skill SHOULD publish

- DatagramRequested
- EndpointResolved
- DatagramSent
- ResponseReceived
- NoResponse
- ExchangeFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The UDP Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [DNS Client](../dns-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The UDP Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- DNS-adjacent discovery skills
- Service discovery skills probing UDP services
- Higher-level datagram protocol skills

---

# Outputs

Typical outputs MAY include

- A bounded datagram exchange result
- Response latency
- Datagram evidence references
- Transport metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The UDP Client Shared Skill SHALL

- Enforce bounded exchanges to prevent amplification and exhaustion
- Respect Rules of Engagement through rate governance
- Avoid amplification abuse by bounding payload sizes and rates
- Protect secret payloads from evidence and logs
- Preserve auditability

UDP can be abused for amplification. The shared skill SHALL enforce strict rate
and size bounds to prevent misuse.

---

# Best Practices

Consumers SHOULD

- Declare idempotency explicitly before enabling retries
- Treat `no_response` as a normal outcome
- Bound response windows tightly
- Reference shared rate policies
- Capture datagram evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Send datagrams directly
- Assume delivery or ordering
- Retry non-idempotent exchanges
- Send large datagrams that enable amplification
- Interpret application protocols in the UDP layer

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
- adr/ADR-001-udp-transport-abstraction.md

---

# Related Shared Packages

- [TCP Client](../tcp-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [DNS Client](../dns-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [Rate Limit Policy](../../../schemas/rate-limit-policy.md)
- [Retry Policy](../../../schemas/retry-policy.md)
- [Proxy Configuration](../../../schemas/proxy-configuration.md)

---

# Architecture Decisions

- [ADR-001 — UDP Transport Abstraction](adr/ADR-001-udp-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Multi-response collection windows
- Datagram fragmentation awareness
- Broadcast and multicast descriptors under strict governance

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant UDP Client Shared Skill provides a bounded, governed, and
implementation-independent UDP transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable datagram exchange while preventing amplification
abuse and making UDP's unreliability explicit, without embedding application
semantics in consumers.
