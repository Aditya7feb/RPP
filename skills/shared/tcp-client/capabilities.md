# TCP Client Capabilities

**File:** `skills/shared/tcp-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the TCP Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[TCP Client Interface](interface.md).

---

# Capability Model

```
Resolution

Connection

Exchange

Governance

Observability
```

---

# Resolution Capabilities

## Endpoint Resolution

The TCP Client SHALL resolve a hostname to an address through the
[DNS Client](../dns-client/README.md).

---

## Address Passthrough

The TCP Client SHALL use a supplied address directly without resolution.

---

# Connection Capabilities

## Connection Establishment

The TCP Client SHALL establish a bounded TCP connection to a host and port.

---

## Proxy Routing

The TCP Client SHALL route connections through the
[Proxy](../proxy/README.md) shared skill where a proxy applies.

---

## Timeout Enforcement

The TCP Client SHALL enforce connection, read, write, and total deadlines.

---

# Exchange Capabilities

## Byte Exchange

The TCP Client SHALL exchange byte streams with bounded read and write
operations.

---

## Half-Close

The TCP Client SHALL support closing the write direction while continuing to
read where the caller requests it.

---

# Governance Capabilities

## Rate Governance

The TCP Client SHALL acquire a rate permit for each connection attempt through
the [Rate Limiter](../rate-limiter/README.md).

---

## Retry Governance

The TCP Client MAY recover transient failures through the
[Retry](../retry/README.md) shared skill, acquiring a fresh permit per attempt.

---

# Observability Capabilities

## Evidence Capture

The TCP Client SHOULD capture connection evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The TCP Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The TCP Client SHOULD expose metrics including connections established, failed,
bytes sent, bytes received, and connect latency.

---

# Capability Boundaries

The TCP Client SHALL NOT

- Interpret application protocols
- Perform TLS negotiation
- Produce findings
- Enumerate ports
- Persist secret payloads

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Endpoint Resolution | Resolution | SHALL |
| Address Passthrough | Resolution | SHALL |
| Connection Establishment | Connection | SHALL |
| Proxy Routing | Connection | SHALL |
| Timeout Enforcement | Connection | SHALL |
| Byte Exchange | Exchange | SHALL |
| Half-Close | Exchange | SHALL |
| Rate Governance | Governance | SHALL |
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
- [Evidence Schema](../../../schemas/evidence.md)
