# API Key Authentication Capabilities

**File:** `skills/authentication/api-keys/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the API Key Authentication
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[API Key Authentication Interface](interface.md).

---

# Capability Model

```
Authorization

Placement Observation

Exposure Analysis

Validation Analysis

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

# Placement Observation Capabilities

## Key Placement Observation

The skill SHALL observe where API keys are placed — headers, query strings, or
body — through the [HTTP Client](../../shared/http-client/README.md).

---

## Transport Observation

The skill SHALL observe whether keys are transmitted over secure transport.

---

# Exposure Analysis Capabilities

## Client Exposure Analysis

The skill SHALL analyze whether keys are exposed in client-side code or public
artifacts.

---

## URL Exposure Analysis

The skill SHALL determine whether keys appear in URLs or query strings.

---

# Validation Analysis Capabilities

## Server Validation Analysis

The skill SHALL determine whether the server validates keys correctly.

---

## Scope And Lifecycle Analysis

The skill SHALL assess whether keys carry scope, expiry, and rotation.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify API key weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with key material redacted.

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
- Test token protocols or authorization decisions
- Persist key material
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Key Placement Observation | Placement Observation | SHALL |
| Transport Observation | Placement Observation | SHALL |
| Client Exposure Analysis | Exposure Analysis | SHALL |
| URL Exposure Analysis | Exposure Analysis | SHALL |
| Server Validation Analysis | Validation Analysis | SHALL |
| Scope And Lifecycle Analysis | Validation Analysis | SHALL |
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
