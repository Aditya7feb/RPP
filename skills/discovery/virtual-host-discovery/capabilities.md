# Virtual Host Discovery Capabilities

**File:** `skills/discovery/virtual-host-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Virtual Host Discovery
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Virtual Host Discovery Interface](interface.md).

---

# Capability Model

```
Authorization

Baseline

Host Probing

Differential Analysis

Asset Construction

Weakness Analysis

Observability
```

---

# Authorization Capabilities

## Policy Consultation

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every probe.

---

## Scope Confinement

The skill SHALL probe only in-scope addresses and host names.

---

# Baseline Capabilities

## Baseline Establishment

The skill SHALL establish a baseline response for the target address through the
[HTTP Client](../../shared/http-client/README.md).

---

# Host Probing Capabilities

## Host-Name Probing

The skill SHALL probe candidate host names through the
[HTTP Client](../../shared/http-client/README.md).

---

## Bounded Probing

The skill SHALL bound candidate volume and request rate.

---

# Differential Analysis Capabilities

## Differential Comparison

The skill SHALL compare candidate responses to the baseline to distinguish distinct
virtual hosts.

---

## Wildcard Handling

The skill SHALL detect and discount wildcard responses to reduce false positives.

---

# Asset Construction Capabilities

## Virtual Host Asset Production

The skill SHALL produce canonical `web-application`
[Assets](../../../schemas/asset.md) for distinct virtual hosts.

---

## Relationship Production

The skill SHALL produce `serves`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Weakness Analysis Capabilities

## Hidden-Host Identification

The skill SHALL identify hidden or internal virtual hosts reachable publicly.

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

The skill SHOULD expose metrics including candidates probed, virtual hosts found,
and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Enumerate content within a discovered host
- Exploit discovered hosts
- Produce a Finding without Evidence
- Act on out-of-scope addresses or host names

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Baseline Establishment | Baseline | SHALL |
| Host-Name Probing | Host Probing | SHALL |
| Bounded Probing | Host Probing | SHALL |
| Differential Comparison | Differential Analysis | SHALL |
| Wildcard Handling | Differential Analysis | SHALL |
| Virtual Host Asset Production | Asset Construction | SHALL |
| Relationship Production | Asset Construction | SHALL |
| Provenance Linking | Asset Construction | SHALL |
| Hidden-Host Identification | Weakness Analysis | SHALL |
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
