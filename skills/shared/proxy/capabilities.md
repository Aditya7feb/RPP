# Proxy Capabilities

**File:** `skills/shared/proxy/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Proxy Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Proxy Interface](interface.md).

---

# Capability Model

```
Selection

Bypass

Tunneling

Authentication

Interception Awareness

Governance

Observability
```

---

# Selection Capabilities

## Proxy Resolution

The Proxy Shared Skill SHALL resolve the applicable
[Proxy Configuration](../../../schemas/proxy-configuration.md) for a destination
by evaluating selection rules.

Inputs

- Destination scheme, host, port
- Available proxy configurations

Outputs

- Selected proxy or a direct-channel decision

---

## Most-Specific Matching

The Proxy Shared Skill SHALL select the most specific matching proxy when
multiple configurations apply.

---

# Bypass Capabilities

## Bypass Evaluation

The Proxy Shared Skill SHALL route a destination directly when it matches any
configured bypass host, CIDR, loopback, or link-local rule.

---

## Precedence

The Proxy Shared Skill SHALL evaluate bypass before selection.

---

# Tunneling Capabilities

## Tunnel Establishment

The Proxy Shared Skill SHALL establish a tunnel using the configured proxy
protocol.

Supported protocols

- http
- https
- socks4
- socks5

---

## Protocol Independence

The Proxy Shared Skill SHALL tunnel any caller operation without depending on
the tunneled protocol.

---

# Authentication Capabilities

## Credential Resolution

The Proxy Shared Skill SHALL resolve proxy credentials through the
[Authentication](../authentication/README.md) shared package using a
`credential_ref`.

---

## Secret Protection

The Proxy Shared Skill SHALL NOT expose, log, or record proxy secrets.

---

# Interception Awareness Capabilities

## Interception Notification

The Proxy Shared Skill SHALL inform the [TLS Client](../tls-client/README.md)
when a configuration declares TLS interception.

---

## Validation Boundary Preservation

The Proxy Shared Skill SHALL NOT accept or reject the tunneled endpoint
certificate; that decision remains with the TLS Client.

---

# Governance Capabilities

## Failure Behavior Enforcement

The Proxy Shared Skill SHALL apply the configured `on_failure` behavior and
SHALL default to `fail`.

---

## Rules of Engagement Compliance

The Proxy Shared Skill SHALL permit direct fallback only where Rules of
Engagement allow direct egress.

---

# Observability Capabilities

## Evidence Capture

The Proxy Shared Skill SHOULD capture routing evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Proxy Shared Skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Proxy Shared Skill SHOULD expose metrics including tunnels established,
bypasses applied, direct fallbacks, and authentication outcomes.

---

# Capability Boundaries

The Proxy Shared Skill SHALL NOT

- Execute the tunneled operation
- Interpret tunneled payloads
- Validate tunneled TLS certificates
- Produce security findings
- Own session state beyond the tunnel

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Proxy Resolution | Selection | SHALL |
| Most-Specific Matching | Selection | SHALL |
| Bypass Evaluation | Bypass | SHALL |
| Precedence | Bypass | SHALL |
| Tunnel Establishment | Tunneling | SHALL |
| Protocol Independence | Tunneling | SHALL |
| Credential Resolution | Authentication | SHALL |
| Secret Protection | Authentication | SHALL |
| Interception Notification | Interception | SHALL |
| Validation Boundary Preservation | Interception | SHALL |
| Failure Behavior Enforcement | Governance | SHALL |
| Rules of Engagement Compliance | Governance | SHALL |
| Evidence Capture | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)
