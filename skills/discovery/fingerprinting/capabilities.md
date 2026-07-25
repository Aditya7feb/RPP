# Fingerprinting Capabilities

**File:** `skills/discovery/fingerprinting/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Fingerprinting Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Fingerprinting Interface](interface.md).

---

# Capability Model

```
Authorization

Signal Collection

Technology Matching

Technology Production

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

The skill SHALL fingerprint only in-scope Assets.

---

# Signal Collection Capabilities

## HTTP Signal Collection

The skill SHALL collect HTTP headers, bodies, and cookies through the
[HTTP Client](../../shared/http-client/README.md).

---

## TLS Signal Collection

The skill SHALL collect TLS facts through the
[TLS Client](../../shared/tls-client/README.md).

---

## Passive Preference

The skill SHALL prefer passive signals and gate active probing.

---

# Technology Matching Capabilities

## Technology Identification

The skill SHALL match signals to technologies and versions.

---

## Confidence Grading

The skill SHALL grade identification confidence, distinguishing certain from
inferred identifications.

---

# Technology Production Capabilities

## Technology Record Production

The skill SHALL produce canonical
[Technology](../../../schemas/technology.md) records.

---

## Asset Linking

The skill SHALL link each Technology to its fingerprinted
[Asset](../../../schemas/asset.md).

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify technology-exposure weaknesses such as outdated versions
and verbose version disclosure.

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

The skill SHOULD expose metrics including technologies identified and findings
emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP or TLS input or output directly
- Enumerate content or ports
- Retrieve external vulnerability intelligence directly
- Produce a Finding without Evidence
- Act on out-of-scope Assets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| HTTP Signal Collection | Signal Collection | SHALL |
| TLS Signal Collection | Signal Collection | SHALL |
| Passive Preference | Signal Collection | SHALL |
| Technology Identification | Technology Matching | SHALL |
| Confidence Grading | Technology Matching | SHALL |
| Technology Record Production | Technology Production | SHALL |
| Asset Linking | Technology Production | SHALL |
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
- [Technology Schema](../../../schemas/technology.md)
