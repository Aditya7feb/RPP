# Content Discovery Capabilities

**File:** `skills/discovery/content-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Content Discovery Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Content Discovery Interface](interface.md).

---

# Capability Model

```
Authorization

Path Probing

Link Extraction

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

The skill SHALL probe only in-scope applications and follow only in-scope links.

---

# Path Probing Capabilities

## Candidate-Path Probing

The skill SHALL probe candidate paths through the
[HTTP Client](../../shared/http-client/README.md).

---

## Bounded Crawling

The skill SHALL bound request volume and crawl depth.

---

# Link Extraction Capabilities

## Link Extraction

The skill SHALL extract in-scope links from responses.

---

## Response Classification

The skill SHALL classify responses to distinguish present, absent, and redirected
content.

---

# Asset Construction Capabilities

## Endpoint Asset Production

The skill SHALL produce canonical `endpoint` and `web-application`
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

The skill SHALL identify content-exposure weaknesses such as directory listing and
exposed backup files.

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

The skill SHOULD expose metrics including paths probed, endpoints found, and
findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Fingerprint technologies in depth
- Exploit content
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Candidate-Path Probing | Path Probing | SHALL |
| Bounded Crawling | Path Probing | SHALL |
| Link Extraction | Link Extraction | SHALL |
| Response Classification | Link Extraction | SHALL |
| Endpoint Asset Production | Asset Construction | SHALL |
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
