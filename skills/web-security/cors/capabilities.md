# CORS Capabilities

**File:** `skills/web-security/cors/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the CORS Skill. Capabilities
describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[CORS Interface](interface.md).

---

# Capability Model

```
Authorization

Cross-Origin Observation

Reflection Analysis

Credential Analysis

Permission Analysis

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

# Cross-Origin Observation Capabilities

## Origin Response Observation

The skill SHALL observe cross-origin response headers through the
[HTTP Client](../../shared/http-client/README.md).

---

# Reflection Analysis Capabilities

## Origin Reflection Analysis

The skill SHALL determine whether an arbitrary `Origin` is reflected into
`Access-Control-Allow-Origin`.

---

## Null Origin Analysis

The skill SHALL determine whether the `null` origin is accepted as trusted.

---

# Credential Analysis Capabilities

## Credentialed Access Analysis

The skill SHALL determine whether credentialed cross-origin access is permitted from
untrusted origins.

---

## Wildcard With Credentials Analysis

The skill SHALL determine whether a wildcard origin is combined with credentials.

---

# Permission Analysis Capabilities

## Method And Header Analysis

The skill SHALL determine whether allowed methods and headers are overly permissive.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify CORS weaknesses from observed behavior and classify them
using canonical weakness identifiers such as CWE-942.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md).

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
- Evaluate full CSP or CSRF defenses
- Perform destructive exploitation
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Origin Response Observation | Cross-Origin Observation | SHALL |
| Origin Reflection Analysis | Reflection Analysis | SHALL |
| Null Origin Analysis | Reflection Analysis | SHALL |
| Credentialed Access Analysis | Credential Analysis | SHALL |
| Wildcard With Credentials Analysis | Credential Analysis | SHALL |
| Method And Header Analysis | Permission Analysis | SHALL |
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
- [HTTP Header Schema](../../../schemas/http-header.md)
