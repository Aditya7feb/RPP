# CSRF Protection Capabilities

**File:** `skills/authentication/csrf/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the CSRF Protection Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[CSRF Protection Interface](interface.md).

---

# Capability Model

```
Authorization

Token Observation

Validation Analysis

Origin Protection Analysis

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

# Token Observation Capabilities

## Token Issuance Observation

The skill SHALL observe anti-CSRF token issuance on state-changing endpoints
through the [HTTP Client](../../shared/http-client/README.md).

---

## Method Observation

The skill SHALL observe whether state changes are reachable by safe HTTP methods.

---

# Validation Analysis Capabilities

## Token Validation Analysis

The skill SHALL determine whether the server validates anti-CSRF tokens.

---

## Session Binding Analysis

The skill SHALL determine whether tokens are bound to the session and non-replayable.

---

# Origin Protection Analysis Capabilities

## Same-Site Analysis

The skill SHALL determine whether same-site cookie protections are present.

---

## Origin Check Analysis

The skill SHALL determine whether origin or referer validation is present.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify CSRF weaknesses from observed behavior.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with tokens redacted.

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
- Execute harmful state changes
- Test authorization decisions
- Persist tokens or secrets
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Token Issuance Observation | Token Observation | SHALL |
| Method Observation | Token Observation | SHALL |
| Token Validation Analysis | Validation Analysis | SHALL |
| Session Binding Analysis | Validation Analysis | SHALL |
| Same-Site Analysis | Origin Protection Analysis | SHALL |
| Origin Check Analysis | Origin Protection Analysis | SHALL |
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
