# Clickjacking Capabilities

**File:** `skills/web-security/clickjacking/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Clickjacking Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Clickjacking Interface](interface.md).

---

# Capability Model

```
Authorization

Response Observation

Framing Control Analysis

Sensitivity Analysis

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

The skill SHALL test only in-scope applications.

---

# Response Observation Capabilities

## Header Observation

The skill SHALL observe response headers through the
[HTTP Client](../../shared/http-client/README.md).

---

# Framing Control Analysis Capabilities

## X-Frame-Options Analysis

The skill SHALL analyze the `X-Frame-Options` header.

---

## Frame-Ancestors Analysis

The skill SHALL analyze the Content Security Policy `frame-ancestors` directive.

---

# Sensitivity Analysis Capabilities

## Page Sensitivity Analysis

The skill SHALL identify sensitive state-changing pages that are framable.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify clickjacking weaknesses from observed behavior and
classify them using canonical weakness identifiers such as CWE-1021.

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
- Evaluate full CSP or CORS
- Perform destructive exploitation
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Header Observation | Response Observation | SHALL |
| X-Frame-Options Analysis | Framing Control Analysis | SHALL |
| Frame-Ancestors Analysis | Framing Control Analysis | SHALL |
| Page Sensitivity Analysis | Sensitivity Analysis | SHALL |
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
