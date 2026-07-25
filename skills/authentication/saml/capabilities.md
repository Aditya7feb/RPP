# SAML Authentication Capabilities

**File:** `skills/authentication/saml/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the SAML Authentication Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[SAML Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Assertion Observation

Signature Analysis

Restriction Analysis

Replay Analysis

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

# Assertion Observation Capabilities

## Assertion Consumption Observation

The skill SHALL observe how the service provider consumes assertions through the
[HTTP Client](../../shared/http-client/README.md).

---

## Binding Observation

The skill SHALL observe the SAML binding and transport security.

---

# Signature Analysis Capabilities

## Signature Validation Analysis

The skill SHALL determine whether assertion signatures are validated.

---

## Signature Wrapping Analysis

The skill SHALL determine whether XML signature wrapping is accepted.

---

## Signature Stripping Analysis

The skill SHALL determine whether removed signatures are detected.

---

# Restriction Analysis Capabilities

## Audience Restriction Analysis

The skill SHALL determine whether audience restrictions are enforced.

---

## Recipient And Destination Analysis

The skill SHALL determine whether recipient and destination are validated.

---

# Replay Analysis Capabilities

## Replay Protection Analysis

The skill SHALL determine whether assertion replay is rejected through identifier
and timestamp validation.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify SAML weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with assertions and signing
material redacted.

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
- Discover applications or endpoints
- Evaluate OAuth2 or OIDC flows
- Persist assertions or signing material
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Assertion Consumption Observation | Assertion Observation | SHALL |
| Binding Observation | Assertion Observation | SHALL |
| Signature Validation Analysis | Signature Analysis | SHALL |
| Signature Wrapping Analysis | Signature Analysis | SHALL |
| Signature Stripping Analysis | Signature Analysis | SHALL |
| Audience Restriction Analysis | Restriction Analysis | SHALL |
| Recipient And Destination Analysis | Restriction Analysis | SHALL |
| Replay Protection Analysis | Replay Analysis | SHALL |
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
