# OIDC Authentication Capabilities

**File:** `skills/authentication/oidc/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the OIDC Authentication Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[OIDC Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Discovery Observation

ID Token Analysis

Nonce And Claim Analysis

UserInfo Analysis

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

# Discovery Observation Capabilities

## Discovery Document Observation

The skill SHALL observe the OpenID discovery document and JWKS exposure through the
[HTTP Client](../../shared/http-client/README.md).

---

## Provider Metadata Observation

The skill SHALL observe provider metadata relevant to identity validation.

---

# ID Token Analysis Capabilities

## Signature Validation Analysis

The skill SHALL determine whether the relying party validates ID token signatures.

---

## Audience And Issuer Analysis

The skill SHALL determine whether audience and issuer claims are validated.

---

# Nonce And Claim Analysis Capabilities

## Nonce Analysis

The skill SHALL determine whether a `nonce` is required and validated.

---

## Identity Claim Analysis

The skill SHALL determine whether identity claims are verified before trust.

---

# UserInfo Analysis Capabilities

## UserInfo Handling Analysis

The skill SHALL determine whether the UserInfo endpoint is served securely and with
proper authorization.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify OIDC weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with ID tokens and secrets
redacted.

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
- Re-evaluate OAuth2 authorization-flow specifics or JWT structure in depth
- Persist ID tokens or secrets
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Discovery Document Observation | Discovery Observation | SHALL |
| Provider Metadata Observation | Discovery Observation | SHALL |
| Signature Validation Analysis | ID Token Analysis | SHALL |
| Audience And Issuer Analysis | ID Token Analysis | SHALL |
| Nonce Analysis | Nonce And Claim Analysis | SHALL |
| Identity Claim Analysis | Nonce And Claim Analysis | SHALL |
| UserInfo Handling Analysis | UserInfo Analysis | SHALL |
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
- [OAuth2 Authentication](../oauth2/README.md)
