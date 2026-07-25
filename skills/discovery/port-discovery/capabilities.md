# Port Discovery Capabilities

**File:** `skills/discovery/port-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Port Discovery Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Port Discovery Interface](interface.md).

---

# Capability Model

```
Authorization

Probing

State Classification

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

The skill SHALL probe only in-scope hosts.

---

# Probing Capabilities

## TCP Probing

The skill SHALL probe TCP ports through the
[TCP Client](../../shared/tcp-client/README.md).

---

## UDP Probing

The skill SHALL probe UDP ports through the
[UDP Client](../../shared/udp-client/README.md).

---

## Bounded Probing

The skill SHALL bound port ranges and probe rate.

---

# State Classification Capabilities

## Port-State Classification

The skill SHALL classify port state as open, closed, or filtered from
connectivity results.

---

# Asset Construction Capabilities

## Asset Production

The skill SHALL produce canonical `port` and `service`
[Assets](../../../schemas/asset.md).

---

## Relationship Production

The skill SHALL produce `exposes` and `serves`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

## Provenance Linking

The skill SHALL link every Asset to its Observations and Evidence.

---

# Weakness Analysis Capabilities

## Exposure Identification

The skill SHALL identify exposure weaknesses such as administrative or plaintext
services exposed to untrusted networks.

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

The skill SHOULD expose metrics including ports probed, services found, and
findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform socket input or output directly
- Fingerprint service software in depth
- Exploit services
- Produce a Finding without Evidence
- Act on out-of-scope hosts

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| TCP Probing | Probing | SHALL |
| UDP Probing | Probing | SHALL |
| Bounded Probing | Probing | SHALL |
| Port-State Classification | State Classification | SHALL |
| Asset Production | Asset Construction | SHALL |
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
- [TCP Client](../../shared/tcp-client/README.md)
