# XML External Entity Capabilities

**File:** `skills/web-security/xxe/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the XML External Entity Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[XML External Entity Interface](interface.md).

---

# Capability Model

```
Authorization

Entity Probing

Resolution Analysis

Out-Of-Band Analysis

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

# Entity Probing Capabilities

## Bounded Entity Probing

The skill SHALL submit bounded, non-sensitive entity probes through the
[HTTP Client](../../shared/http-client/README.md).

---

# Resolution Analysis Capabilities

## In-Band Resolution Analysis

The skill SHALL determine whether a bounded, non-sensitive entity is resolved in the
response.

---

# Out-Of-Band Analysis Capabilities

## Interaction Analysis

The skill SHALL determine whether an out-of-band interaction to a controlled collector
confirms external-entity resolution.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify XXE weaknesses from observed behavior and classify them using
canonical weakness identifiers such as CWE-611.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only non-sensitive resolution
recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including endpoints tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test general request forgery
- Read, exfiltrate, or modify sensitive files
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Entity Probing | Entity Probing | SHALL |
| In-Band Resolution Analysis | Resolution Analysis | SHALL |
| Interaction Analysis | Out-Of-Band Analysis | SHALL |
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
