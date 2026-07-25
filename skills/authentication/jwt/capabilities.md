# JWT Authentication Capabilities

**File:** `skills/authentication/jwt/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the JWT Authentication Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[JWT Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Token Observation

Structure Analysis

Signature Analysis

Claim Analysis

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

The skill SHALL test only in-scope targets.

---

# Token Observation Capabilities

## Token Issuance Observation

The skill SHALL observe how tokens are issued through the
[HTTP Client](../../shared/http-client/README.md).

---

## Token Acceptance Observation

The skill SHALL observe how modified tokens are accepted or rejected.

---

## Transport Observation

The skill SHALL observe whether tokens are transmitted over secure transport.

---

# Structure Analysis Capabilities

## Header And Algorithm Analysis

The skill SHALL analyze the token header and declared signing algorithm.

---

## Payload Confidentiality Analysis

The skill SHALL determine whether sensitive data is disclosed in the payload.

---

# Signature Analysis Capabilities

## Signature Validation Analysis

The skill SHALL determine whether the server verifies token signatures.

---

## Algorithm Confusion Analysis

The skill SHALL determine whether algorithm confusion is accepted.

---

## Bounded Secret Analysis

The skill SHALL assess weak HMAC secrets only within configured, bounded limits.

---

# Claim Analysis Capabilities

## Expiry Analysis

The skill SHALL determine whether expiry claims are enforced.

---

## Issuer And Audience Analysis

The skill SHALL determine whether issuer and audience claims are validated.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify JWT weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with token secrets redacted.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including checks performed and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints
- Recover secrets through unbounded brute force
- Test protocol flows or authorization decisions
- Persist token secrets
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Token Issuance Observation | Token Observation | SHALL |
| Token Acceptance Observation | Token Observation | SHALL |
| Transport Observation | Token Observation | SHALL |
| Header And Algorithm Analysis | Structure Analysis | SHALL |
| Payload Confidentiality Analysis | Structure Analysis | SHALL |
| Signature Validation Analysis | Signature Analysis | SHALL |
| Algorithm Confusion Analysis | Signature Analysis | SHALL |
| Bounded Secret Analysis | Signature Analysis | SHALL |
| Expiry Analysis | Claim Analysis | SHALL |
| Issuer And Audience Analysis | Claim Analysis | SHALL |
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
- [Policy Engine](../../shared/policy-engine/README.md)
