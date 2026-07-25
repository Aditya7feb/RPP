# Mutual TLS Authentication Capabilities

**File:** `skills/authentication/mtls/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Mutual TLS Authentication
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Mutual TLS Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Handshake Observation

Validation Analysis

Revocation Analysis

Fallback Analysis

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action.

---

## Scope Confinement

The skill SHALL test only in-scope services.

---

# Handshake Observation Capabilities

## Certificate Requirement Observation

The skill SHALL observe whether a client certificate is required through the
[TLS Client](../../shared/tls-client/README.md).

---

## Application Behavior Observation

The skill SHALL observe application behavior with and without a client certificate
through the [HTTP Client](../../shared/http-client/README.md).

---

# Validation Analysis Capabilities

## Certificate Validation Analysis

The skill SHALL determine whether untrusted, self-signed, or expired certificates
are accepted, using the canonical
[TLS Validation Result](../../../schemas/tls-validation-result.md).

---

## Identity Binding Analysis

The skill SHALL determine whether certificate subject or SAN is validated against
the expected identity.

---

# Revocation Analysis Capabilities

## Revocation Checking Analysis

The skill SHALL determine whether revoked certificates are rejected.

---

# Fallback Analysis Capabilities

## Fallback Detection

The skill SHALL determine whether the service falls back to unauthenticated or
weaker authentication.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify mutual TLS weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with private key material redacted.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including checks performed and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Open TLS connections or perform HTTP input or output directly
- Discover services or certificates
- Analyze general server-side TLS posture
- Persist private key material
- Produce a Finding without Evidence
- Act on out-of-scope services

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Certificate Requirement Observation | Handshake Observation | SHALL |
| Application Behavior Observation | Handshake Observation | SHALL |
| Certificate Validation Analysis | Validation Analysis | SHALL |
| Identity Binding Analysis | Validation Analysis | SHALL |
| Revocation Checking Analysis | Revocation Analysis | SHALL |
| Fallback Detection | Fallback Analysis | SHALL |
| Weakness Identification | Weakness Analysis | SHALL |
| Finding Production | Weakness Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [TLS Validation Result Schema](../../../schemas/tls-validation-result.md)
