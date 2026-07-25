# FTP Client Capabilities

**File:** `skills/shared/ftp-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the FTP Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[FTP Client Interface](interface.md).

---

# Capability Model

```
Control Channel

Data Channel

Security

Authentication

Command Exchange

Governance

Observability
```

---

# Control Channel Capabilities

## Control Establishment

The FTP Client SHALL establish the control channel through the
[TCP Client](../tcp-client/README.md).

---

## Greeting Handling

The FTP Client SHALL read and record the server greeting.

---

# Data Channel Capabilities

## Passive Data Channel

The FTP Client SHALL open passive data channels.

---

## Active Data Channel

The FTP Client SHALL open active data channels where configured and permitted.

---

## Bounded Transfer

The FTP Client SHALL bound transfer sizes.

---

# Security Capabilities

## Explicit FTPS

The FTP Client SHALL upgrade to TLS via `AUTH TLS` through the
[TLS Client](../tls-client/README.md).

---

## Cleartext Refusal

The FTP Client SHALL refuse to continue where confidentiality is required and
TLS is unavailable.

---

# Authentication Capabilities

## Credential Resolution

The FTP Client SHALL resolve credentials through the
[Authentication](../authentication/README.md) package.

---

## Anonymous Access

The FTP Client SHALL support anonymous authentication where explicitly requested
and SHALL report it as data.

---

# Command Exchange Capabilities

## Command Exchange

The FTP Client SHALL exchange FTP commands and record replies.

---

## Reply Mapping

The FTP Client SHALL map reply codes to canonical outcomes.

---

# Governance Capabilities

## Rate And Proxy Governance

The FTP Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Intrusive Operation Gating

The FTP Client SHALL gate write and delete operations as intrusive.

---

## Retry Governance

The FTP Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The FTP Client SHOULD capture session evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The FTP Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The FTP Client SHOULD expose metrics including sessions, transfers, bytes
transferred, and session duration.

---

# Capability Boundaries

The FTP Client SHALL NOT

- Detect anonymous-write or other vulnerabilities
- Produce findings
- Perform unauthorized writes
- Persist credentials or file contents without authorization

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Control Establishment | Control Channel | SHALL |
| Greeting Handling | Control Channel | SHALL |
| Passive Data Channel | Data Channel | SHALL |
| Active Data Channel | Data Channel | SHALL |
| Bounded Transfer | Data Channel | SHALL |
| Explicit FTPS | Security | SHALL |
| Cleartext Refusal | Security | SHALL |
| Credential Resolution | Authentication | SHALL |
| Anonymous Access | Authentication | SHALL |
| Command Exchange | Command Exchange | SHALL |
| Reply Mapping | Command Exchange | SHALL |
| Rate And Proxy Governance | Governance | SHALL |
| Intrusive Operation Gating | Governance | SHALL |
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
