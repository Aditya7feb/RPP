# DNS Enumeration Capabilities

**File:** `skills/discovery/dns-enumeration/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the DNS Enumeration Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[DNS Enumeration Interface](interface.md).

---

# Capability Model

```
Authorization

Record Enumeration

Asset Construction

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

The skill SHALL query only in-scope targets.

---

# Record Enumeration Capabilities

## Record Query

The skill SHALL enumerate DNS record types through the
[DNS Client](../../shared/dns-client/README.md).

---

## Name Resolution

The skill SHALL resolve names to addresses and services.

---

# Asset Construction Capabilities

## Asset Production

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) for
domains, subdomains, hosts, addresses, and services.

---

## Relationship Production

The skill SHALL produce canonical
[Asset Relationships](../../../schemas/asset-relationship.md) such as
`resolves-to` and `serves`.

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify DNS-related weaknesses such as zone-transfer exposure and
dangling records.

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

The skill SHOULD expose metrics including records enumerated, assets produced, and
findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform DNS input or output directly
- Brute-force subdomains
- Exploit weaknesses
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Record Query | Record Enumeration | SHALL |
| Name Resolution | Record Enumeration | SHALL |
| Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Provenance Linking | Asset Construction | SHALL |
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
- [DNS Client](../../shared/dns-client/README.md)
