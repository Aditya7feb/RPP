# SSH Client Capabilities

**File:** `skills/shared/ssh-client/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the SSH Client Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[SSH Client Interface](interface.md).

---

# Capability Model

```
Transport

Host-Key Trust

Authentication

Channels

Execution

Governance

Observability
```

---

# Transport Capabilities

## Transport Establishment

The SSH Client SHALL establish the transport through the
[TCP Client](../tcp-client/README.md).

---

## Algorithm Negotiation

The SSH Client SHALL negotiate and record transport algorithms as data.

---

# Host-Key Trust Capabilities

## Host-Key Verification

The SSH Client SHALL verify the host key against a configured trust policy.

---

## Fingerprint Recording

The SSH Client SHALL record the host-key fingerprint as data.

---

# Authentication Capabilities

## Credential Resolution

The SSH Client SHALL resolve credentials through the
[Authentication](../authentication/README.md) package.

---

## Method Support

The SSH Client SHALL support password, public-key, keyboard-interactive, and
agent authentication.

---

# Channel Capabilities

## Command Channel

The SSH Client SHALL open command-execution channels.

---

## Subsystem Channel

The SSH Client SHALL open subsystem channels such as SFTP.

---

## Port Forwarding

The SSH Client SHALL open local and remote forwarding where explicitly
configured.

---

# Execution Capabilities

## Bounded Execution

The SSH Client SHALL execute authorized commands with bounded output.

---

## Intrusive Gating

The SSH Client SHALL gate command and shell execution as intrusive.

---

# Governance Capabilities

## Rate And Proxy Governance

The SSH Client SHALL apply rate and proxy governance through the
[Rate Limiter](../rate-limiter/README.md) and [Proxy](../proxy/README.md) shared
skills.

---

## Attempt Bounding

The SSH Client SHALL bound authentication attempts.

---

## Retry Governance

The SSH Client MAY retry transient transport failures through the
[Retry](../retry/README.md) shared skill.

---

# Observability Capabilities

## Evidence Capture

The SSH Client SHOULD capture session evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The SSH Client SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The SSH Client SHOULD expose metrics including sessions, channels opened,
commands executed, and session duration.

---

# Capability Boundaries

The SSH Client SHALL NOT

- Detect weak algorithms or other vulnerabilities
- Produce findings
- Brute-force credentials
- Execute unauthorized commands
- Persist credentials, private keys, or unauthorized output

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Transport Establishment | Transport | SHALL |
| Algorithm Negotiation | Transport | SHALL |
| Host-Key Verification | Host-Key Trust | SHALL |
| Fingerprint Recording | Host-Key Trust | SHALL |
| Credential Resolution | Authentication | SHALL |
| Method Support | Authentication | SHALL |
| Command Channel | Channels | SHALL |
| Subsystem Channel | Channels | SHALL |
| Port Forwarding | Channels | SHALL |
| Bounded Execution | Execution | SHALL |
| Intrusive Gating | Execution | SHALL |
| Rate And Proxy Governance | Governance | SHALL |
| Attempt Bounding | Governance | SHALL |
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
