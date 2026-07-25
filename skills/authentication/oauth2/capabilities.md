# OAuth2 Authentication Capabilities

**File:** `skills/authentication/oauth2/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the OAuth2 Authentication
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[OAuth2 Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Flow Observation

Redirect Analysis

State And PKCE Analysis

Token Handling Analysis

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

# Flow Observation Capabilities

## Grant Type Observation

The skill SHALL observe the OAuth2 grant types offered through the
[HTTP Client](../../shared/http-client/README.md).

---

## Authorization And Token Endpoint Observation

The skill SHALL observe authorization and token endpoint behavior.

---

# Redirect Analysis Capabilities

## Redirect URI Validation Analysis

The skill SHALL determine whether redirect URIs are strictly validated, using the
canonical [HTTP Redirect](../../../schemas/http-redirect.md) representation.

---

# State And PKCE Analysis Capabilities

## State Parameter Analysis

The skill SHALL determine whether an anti-forgery `state` parameter is present and
validated.

---

## PKCE Analysis

The skill SHALL determine whether PKCE is enforced for Authorization Code clients.
PKCE SHOULD be used for all Authorization Code clients, including both public and
confidential clients, consistent with current OAuth security guidance.

---

# Token Handling Analysis Capabilities

## Token Transport Analysis

The skill SHALL determine whether tokens are transported securely.

---

## Scope Enforcement Analysis

The skill SHALL determine whether granted scopes are enforced and least-privilege.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify OAuth2 weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with tokens and client secrets
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
- Evaluate OIDC identity-layer specifics or JWT structure in depth
- Persist tokens or client secrets
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Grant Type Observation | Flow Observation | SHALL |
| Authorization And Token Endpoint Observation | Flow Observation | SHALL |
| Redirect URI Validation Analysis | Redirect Analysis | SHALL |
| State Parameter Analysis | State And PKCE Analysis | SHALL |
| PKCE Analysis | State And PKCE Analysis | SHALL |
| Token Transport Analysis | Token Handling Analysis | SHALL |
| Scope Enforcement Analysis | Token Handling Analysis | SHALL |
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
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
