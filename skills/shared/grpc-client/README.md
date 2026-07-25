# gRPC Client Shared Skill

**File:** `skills/shared/grpc-client/README.md`

**Version:** 1.0.0

---

# Purpose

The gRPC Client Shared Skill provides the canonical, implementation-independent
mechanism for invoking gRPC methods within the Robust PenTest Platform (RPP).

Rather than allowing individual skills to construct gRPC calls directly, this
shared skill centralizes channel establishment, method invocation, streaming,
metadata handling, status mapping, governance, and observability.

All packages that require gRPC transport SHALL delegate to this shared skill.

---

# Goals

The gRPC Client Shared Skill SHALL

- Abstract gRPC transport behind a stable interface
- Establish HTTP/2 channels through the [HTTP Client](../http-client/README.md)
- Secure channels through the [TLS Client](../tls-client/README.md)
- Invoke unary and streaming methods
- Carry and observe call metadata
- Map gRPC status codes to canonical outcomes
- Produce gRPC evidence
- Integrate with platform observability

---

# Non-Goals

The gRPC Client Shared Skill SHALL NOT

- Interpret message semantics
- Detect vulnerabilities
- Produce security findings
- Compile or interpret service definitions as findings
- Parse message payloads as findings

The gRPC Client invokes methods and moves messages. Application and security
interpretation belong to domain skills such as an API-security gRPC skill.

---

# Design Principles

The gRPC Client Shared Skill SHALL be

- Deterministic in bounds given the same configuration and inputs
- Layered atop existing HTTP/2 and TLS shared skills
- Bounded in message size and call duration
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

gRPC Client Shared Skill

├── Channel Coordinator     → HTTP Client (HTTP/2)
├── Secure Channel          → TLS Client
├── Method Invoker
├── Stream Manager
├── Metadata Handler
├── Status Mapper
├── Evidence Manager
├── Event Manager

↓

Transport Adapter
```

The gRPC Client invokes methods but SHALL remain unaware of the transport
adapter implementation.

---

# Responsibilities

The gRPC Client Shared Skill is responsible for

- Establishing an HTTP/2 channel via the
  [HTTP Client](../http-client/README.md)
- Securing the channel via the [TLS Client](../tls-client/README.md)
- Invoking unary, server-streaming, client-streaming, and bidirectional methods
- Carrying request metadata and observing response metadata and trailers
- Mapping gRPC status codes to canonical outcomes
- Applying rate, retry, and proxy governance
- Emitting gRPC lifecycle events and capturing evidence

---

# Invocation Lifecycle

```
Receive Invoke Request

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
```

The call outcome SHOULD be preserved as evidence.

---

# Method Kinds

The gRPC Client SHALL support

- unary
- server_streaming
- client_streaming
- bidirectional_streaming

Streaming methods SHALL be bounded by message counts, sizes, and a total call
deadline.

---

# Metadata And Trailers

The gRPC Client SHALL carry caller-supplied request metadata and SHALL observe
response metadata and trailers.

Metadata SHALL NOT contain inline secrets; credentials SHALL be referenced
through the [Authentication](../authentication/README.md) shared package.

---

# Status Mapping

The gRPC Client SHALL map gRPC status codes to canonical outcomes.

- `OK` maps to a successful outcome
- Retryable statuses such as `UNAVAILABLE` map to retryable errors
- Non-retryable statuses map to non-retryable errors

Status interpretation as a security weakness SHALL remain the responsibility of
domain skills.

---

# Governance

The gRPC Client SHALL

- Acquire a permit from the [Rate Limiter](../rate-limiter/README.md) per call,
  including retries
- Route through the [Proxy](../proxy/README.md) shared skill where configured
- Recover retryable statuses through the [Retry](../retry/README.md) shared skill

Deadlines SHALL bound every call.

---

# Evidence

The gRPC Client Shared Skill SHOULD capture

- Method and channel target
- Request and response message counts and sizes
- gRPC status and trailers
- Call duration

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secret
payloads or metadata.

---

# Events

The gRPC Client Shared Skill SHOULD publish

- CallStarted
- ChannelEstablished
- MessageSent
- MessageReceived
- CallCompleted
- CallFailed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The gRPC Client Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Proxy](../proxy/README.md)
- [Evidence Schema](../../../schemas/evidence.md)

The gRPC Client Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- API-security gRPC skills
- Service enumeration skills probing gRPC endpoints

---

# Outputs

Typical outputs MAY include

- A bounded call result
- gRPC status and trailers
- Call metrics
- gRPC evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The gRPC Client Shared Skill SHALL

- Bound message sizes and call duration
- Respect Rules of Engagement through rate and proxy governance
- Protect secret metadata and payloads from evidence and logs
- Report status codes as data, not findings
- Preserve auditability

Unbounded streaming can exhaust resources. The shared skill SHALL enforce
bounds.

---

# Best Practices

Consumers SHOULD

- Bound streaming message counts and sizes
- Set explicit deadlines
- Reference shared rate, retry, and proxy policies
- Reference credentials rather than inlining metadata secrets
- Capture call evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Construct gRPC calls directly
- Stream without bounds
- Embed secrets in metadata
- Interpret status codes as findings within the transport layer
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
- adr/ADR-001-grpc-transport-abstraction.md

---

# Related Shared Packages

- [HTTP Client](../http-client/README.md)
- [TLS Client](../tls-client/README.md)
- [WebSocket Client](../websocket-client/README.md)
- [Proxy](../proxy/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)
- [TLS Session](../../../schemas/tls-session.md)

---

# Architecture Decisions

- [ADR-001 — gRPC Transport Abstraction](adr/ADR-001-grpc-transport-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Reflection-based method discovery expressed as canonical descriptors
- Compression negotiation detail
- Deadline propagation across call chains
- Load-balancing policy descriptors

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant gRPC Client Shared Skill provides a bounded, governed, and
implementation-independent gRPC transport abstraction for the Robust PenTest
Platform.

It enables consistent, auditable method invocation atop the existing HTTP/2 and
TLS shared skills, without embedding application semantics or transport
implementations in consumers.
