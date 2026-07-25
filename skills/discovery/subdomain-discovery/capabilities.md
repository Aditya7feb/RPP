# Subdomain Discovery Capabilities

**File:** `skills/discovery/subdomain-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Subdomain Discovery
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Subdomain Discovery Interface](interface.md).

---

# Capability Model

```
Authorization

Passive Collection

Active Resolution

Asset Construction

Takeover Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every active resolution.

---

## Scope Confinement

The skill SHALL confirm every resolved subdomain in-scope.

---

# Passive Collection Capabilities

## Passive Candidate Collection

The skill SHALL collect subdomain candidates from passive sources.

---

## Candidate Generation

The skill SHALL generate bounded active candidates within scope.

---

# Active Resolution Capabilities

## Candidate Resolution

The skill SHALL resolve candidates through the
[DNS Client](../../shared/dns-client/README.md).

---

## Bounded Resolution

The skill SHALL bound candidate volume and resolution rate.

---

# Asset Construction Capabilities

## Subdomain Asset Production

The skill SHALL produce canonical `subdomain`
[Assets](../../../schemas/asset.md), suspected for passive-only and confirmed for
resolved candidates.

---

## Relationship Production

The skill SHALL produce `resolves-to`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Takeover Analysis Capabilities

## Takeover Identification

The skill SHALL identify subdomain-takeover potential from dangling delegations
and CNAMEs.

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

The skill SHOULD expose metrics including candidates evaluated, subdomains
confirmed, and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform DNS input or output directly
- Enumerate all records per name
- Exploit takeover opportunities
- Produce a Finding without Evidence
- Act on out-of-scope domains

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Passive Candidate Collection | Passive Collection | SHALL |
| Candidate Generation | Passive Collection | SHALL |
| Candidate Resolution | Active Resolution | SHALL |
| Bounded Resolution | Active Resolution | SHALL |
| Subdomain Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Provenance Linking | Asset Construction | SHALL |
| Takeover Identification | Takeover Analysis | SHALL |
| Finding Production | Takeover Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [DNS Client](../../shared/dns-client/README.md)
