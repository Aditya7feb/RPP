# gRPC Client Capabilities

**File:** `skills/shared/grpc-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the gRPC Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[gRPC Client Interface](interface.md).

---

# Capability Model

```
Channel

Invocation

Streaming

Metadata

Status

Governance

Observability
```

---

# Channel Capabilities

## Channel Establishment

The gRPC Client SHALL establish an HTTP/2 channel through the
[HTTP Client](../http-client/README.md).

---

## Secure Channel

The gRPC Client SHALL secure channels through the
[TLS Client](../tls-client/README.md).

---

# Invocation Capabilities

## Unary Invocation

The gRPC Client SHALL invoke unary methods.

---

## Deadline Enforcement

The gRPC Client SHALL enforce a per-call deadline.

---

# Streaming Capabilities

## Server Streaming

The gRPC Client SHALL receive bounded server-streamed messages.

---

## Client Streaming

The gRPC Client SHALL send bounded client-streamed messages.

---

## Bidirectional Streaming

The gRPC Client SHALL support bounded bidirectional streaming.

---

# Metadata Capabilities

## Request Metadata

The gRPC Client SHALL carry caller-supplied request metadata.

---

## Response Metadata And Trailers

The gRPC Client SHALL observe response metadata and trailers.

---

# Status Capabilities

## Status Mapping

The gRPC Client SHALL map gRPC status codes to canonical outcomes.

---

# Governance Capabilities

## Rate And Proxy Governance

The gRPC Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The gRPC Client MAY retry retryable statuses through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The gRPC Client SHOULD capture gRPC evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The gRPC Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The gRPC Client SHOULD expose metrics including calls, messages sent, messages
received, and call duration.

---

# Capability Boundaries

The gRPC Client SHALL NOT

- Interpret message semantics
- Produce findings
- Authenticate independently
- Persist secret payloads or metadata

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Channel Establishment | Channel | SHALL |
| Secure Channel | Channel | SHALL |
| Unary Invocation | Invocation | SHALL |
| Deadline Enforcement | Invocation | SHALL |
| Server Streaming | Streaming | SHALL |
| Client Streaming | Streaming | SHALL |
| Bidirectional Streaming | Streaming | SHALL |
| Request Metadata | Metadata | SHALL |
| Response Metadata And Trailers | Metadata | SHALL |
| Status Mapping | Status | SHALL |
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
