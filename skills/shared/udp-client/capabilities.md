# UDP Client Capabilities

**File:** `skills/shared/udp-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the UDP Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[UDP Client Interface](interface.md).

---

# Capability Model

```
Resolution

Datagram Exchange

Correlation

Governance

Observability
```

---

# Resolution Capabilities

## Endpoint Resolution

The UDP Client SHALL resolve a hostname to an address through the
[DNS Client](../dns-client/README.md).

---

## Address Passthrough

The UDP Client SHALL use a supplied address directly without resolution.

---

# Datagram Exchange Capabilities

## Datagram Send

The UDP Client SHALL send a bounded datagram to a host and port.

---

## Response Window

The UDP Client SHALL await a response within a bounded window.

---

## No-Response Handling

The UDP Client SHALL return a normal `no_response` outcome when no response
arrives within the window.

---

# Correlation Capabilities

## Response Correlation

The UDP Client SHALL correlate responses to the originating datagram.

---

## Late-Datagram Discard

The UDP Client SHALL discard and record datagrams received outside the window.

---

# Governance Capabilities

## Rate Governance

The UDP Client SHALL acquire a rate permit for each datagram sent through the
[Rate Limiter](../rate-limiter/README.md).

---

## Idempotent Retry

The UDP Client SHALL retry only idempotent exchanges through the
[Retry](../retry/README.md) shared skill.

---

## Amplification Protection

The UDP Client SHALL bound datagram size and rate to prevent amplification
abuse.

---

# Observability Capabilities

## Evidence Capture

The UDP Client SHOULD capture datagram evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The UDP Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The UDP Client SHOULD expose metrics including datagrams sent, responses
received, no-response outcomes, and response latency.

---

# Capability Boundaries

The UDP Client SHALL NOT

- Guarantee delivery or ordering
- Interpret application protocols
- Produce findings
- Enumerate ports
- Persist secret payloads

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Endpoint Resolution | Resolution | SHALL |
| Address Passthrough | Resolution | SHALL |
| Datagram Send | Exchange | SHALL |
| Response Window | Exchange | SHALL |
| No-Response Handling | Exchange | SHALL |
| Response Correlation | Correlation | SHALL |
| Late-Datagram Discard | Correlation | SHALL |
| Rate Governance | Governance | SHALL |
| Idempotent Retry | Governance | SHALL |
| Amplification Protection | Governance | SHALL |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Evidence Schema](../../../schemas/evidence.md)
