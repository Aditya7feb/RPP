# SMTP Client Capabilities

**File:** `skills/shared/smtp-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the SMTP Client Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[SMTP Client Interface](interface.md).

---

# Capability Model

```
Session

Negotiation

Security

Authentication

Command Exchange

Governance

Observability
```

---

# Session Capabilities

## Session Establishment

The SMTP Client SHALL establish a session through the
[TCP Client](../tcp-client/README.md).

---

## Greeting Handling

The SMTP Client SHALL read and record the server greeting.

---

# Negotiation Capabilities

## Capability Negotiation

The SMTP Client SHALL negotiate capabilities via `EHLO`.

---

## Capability Reporting

The SMTP Client SHALL report advertised capabilities as data.

---

# Security Capabilities

## STARTTLS Upgrade

The SMTP Client SHALL upgrade to TLS via `STARTTLS` through the
[TLS Client](../tls-client/README.md).

---

## Cleartext Refusal

The SMTP Client SHALL refuse to continue where confidentiality is required and
TLS is unavailable.

---

# Authentication Capabilities

## Credential Resolution

The SMTP Client SHALL resolve credentials through the
[Authentication](../authentication/README.md) package.

---

## Post-TLS Authentication

The SMTP Client SHALL authenticate only after TLS where confidentiality is
required.

---

# Command Exchange Capabilities

## Command Exchange

The SMTP Client SHALL exchange SMTP commands and record replies.

---

## Reply Mapping

The SMTP Client SHALL map reply codes to canonical outcomes.

---

# Governance Capabilities

## Rate And Proxy Governance

The SMTP Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Retry Governance

The SMTP Client MAY retry transient failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The SMTP Client SHOULD capture session evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The SMTP Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The SMTP Client SHOULD expose metrics including sessions, commands exchanged, and
session duration.

---

# Capability Boundaries

The SMTP Client SHALL NOT

- Detect open relays or other vulnerabilities
- Produce findings
- Send unsolicited mail
- Persist credentials or message bodies without authorization

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Session Establishment | Session | SHALL |
| Greeting Handling | Session | SHALL |
| Capability Negotiation | Negotiation | SHALL |
| Capability Reporting | Negotiation | SHALL |
| STARTTLS Upgrade | Security | SHALL |
| Cleartext Refusal | Security | SHALL |
| Credential Resolution | Authentication | SHALL |
| Post-TLS Authentication | Authentication | SHALL |
| Command Exchange | Command Exchange | SHALL |
| Reply Mapping | Command Exchange | SHALL |
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
