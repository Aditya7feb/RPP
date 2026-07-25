# API Discovery Capabilities

**File:** `skills/discovery/api-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the API Discovery Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[API Discovery Interface](interface.md).

---

# Capability Model

```
Authorization

Definition Location

GraphQL Detection

Base-Path Probing

Asset Construction

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every request.

---

## Scope Confinement

The skill SHALL probe only in-scope targets.

---

# Definition Location Capabilities

## Specification Location

The skill SHALL locate API definitions such as OpenAPI and Swagger documents
through the [HTTP Client](../../shared/http-client/README.md).

---

## Operation Extraction

The skill SHALL extract declared operations from a located specification.

---

# GraphQL Detection Capabilities

## GraphQL Endpoint Detection

The skill SHALL detect GraphQL endpoints.

---

## Introspection Detection

The skill SHALL detect whether GraphQL introspection is exposed.

---

# Base-Path Probing Capabilities

## Base-Path Probing

The skill SHALL probe common API base paths and versions.

---

## Bounded Probing

The skill SHALL bound request volume and rate.

---

# Asset Construction Capabilities

## API Asset Production

The skill SHALL produce canonical `api` and `endpoint`
[Assets](../../../schemas/asset.md).

---

## Relationship Production

The skill SHALL produce `serves` and `references`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Weakness Analysis Capabilities

## Exposure Identification

The skill SHALL identify API-exposure weaknesses such as public specifications and
enabled introspection.

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

The skill SHOULD expose metrics including definitions located, endpoints found,
and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Test API operations for vulnerabilities
- Exploit discovered APIs
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Specification Location | Definition Location | SHALL |
| Operation Extraction | Definition Location | SHALL |
| GraphQL Endpoint Detection | GraphQL Detection | SHALL |
| Introspection Detection | GraphQL Detection | SHALL |
| Base-Path Probing | Base-Path Probing | SHALL |
| Bounded Probing | Base-Path Probing | SHALL |
| API Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Provenance Linking | Asset Construction | SHALL |
| Exposure Identification | Weakness Analysis | SHALL |
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
- [HTTP Client](../../shared/http-client/README.md)
