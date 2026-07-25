# Endpoint Enumeration Capabilities

**File:** `skills/discovery/endpoint-enumeration/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Endpoint Enumeration
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Endpoint Enumeration Interface](interface.md).

---

# Capability Model

```
Authorization

Extraction

Parameter Mining

Asset Construction

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every action.

---

## Scope Confinement

The skill SHALL enumerate only in-scope applications.

---

# Extraction Capabilities

## Rendered Extraction

The skill SHALL extract endpoints and parameters from rendered pages through the
[Browser](../../shared/browser/README.md).

---

## Script Extraction

The skill SHALL extract endpoints and parameters from client-side scripts through
the [HTTP Client](../../shared/http-client/README.md).

---

# Parameter Mining Capabilities

## Parameter Mining

The skill SHALL mine additional parameters within bounds.

---

## Bounded Mining

The skill SHALL bound request volume and rate.

---

# Asset Construction Capabilities

## Endpoint Asset Production

The skill SHALL produce or enrich canonical `endpoint`
[Assets](../../../schemas/asset.md) with parameter facts.

---

## Relationship Production

The skill SHALL produce `references`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Weakness Analysis Capabilities

## Hidden-Parameter Identification

The skill SHALL identify hidden parameters and undocumented endpoints.

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

The skill SHOULD expose metrics including endpoints enriched, parameters found,
and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP or browser input or output directly
- Test parameters for vulnerabilities
- Exploit endpoints
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Rendered Extraction | Extraction | SHALL |
| Script Extraction | Extraction | SHALL |
| Parameter Mining | Parameter Mining | SHALL |
| Bounded Mining | Parameter Mining | SHALL |
| Endpoint Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Provenance Linking | Asset Construction | SHALL |
| Hidden-Parameter Identification | Weakness Analysis | SHALL |
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
- [Browser](../../shared/browser/README.md)
