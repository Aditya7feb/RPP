# Database Client Capabilities

**File:** `skills/shared/database-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Database Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Database Client Interface](interface.md).

---

# Capability Model

```
Connection

Security

Authentication

Execution

Transactions

Results

Governance

Observability
```

---

# Connection Capabilities

## Connection Establishment

The Database Client SHALL establish connections through the
[TCP Client](../tcp-client/README.md).

---

## Engine Abstraction

The Database Client SHALL abstract engine differences behind a uniform
interface.

---

# Security Capabilities

## Transport Encryption

The Database Client SHALL encrypt transport through the
[TLS Client](../tls-client/README.md) where supported.

---

## Cleartext Refusal

The Database Client SHALL refuse to connect in cleartext where encryption is
required.

---

# Authentication Capabilities

## Credential Resolution

The Database Client SHALL resolve credentials through the
[Authentication](../authentication/README.md) package.

---

# Execution Capabilities

## Parameterized Execution

The Database Client SHALL execute statements with bound parameters and SHALL NOT
interpolate values into statement text.

---

## Statement Bounding

The Database Client SHALL bound statement duration.

---

# Transaction Capabilities

## Explicit Transactions

The Database Client SHALL support begin, commit, and rollback.

---

## Intrusive Gating

The Database Client SHALL gate data and schema modification as intrusive.

---

# Result Capabilities

## Bounded Results

The Database Client SHALL bound result sets by rows and bytes.

---

## Result Referencing

The Database Client SHALL store large result sets by reference.

---

# Governance Capabilities

## Rate And Proxy Governance

The Database Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The Database Client MAY retry transient connection failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The Database Client SHOULD capture operation evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Database Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Database Client SHOULD expose metrics including operations, rows returned,
bytes returned, and operation duration.

---

# Capability Boundaries

The Database Client SHALL NOT

- Detect SQL injection or other vulnerabilities
- Produce findings
- Concatenate untrusted input into statements
- Perform unauthorized writes or schema changes
- Persist credentials or sensitive results without authorization

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Connection Establishment | Connection | SHALL |
| Engine Abstraction | Connection | SHALL |
| Transport Encryption | Security | SHALL |
| Cleartext Refusal | Security | SHALL |
| Credential Resolution | Authentication | SHALL |
| Parameterized Execution | Execution | SHALL |
| Statement Bounding | Execution | SHALL |
| Explicit Transactions | Transactions | SHALL |
| Intrusive Gating | Transactions | SHALL |
| Bounded Results | Results | SHALL |
| Result Referencing | Results | SHALL |
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
- [TCP Client](../tcp-client/README.md)
