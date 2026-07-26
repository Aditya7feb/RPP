# Insecure Deserialization Capabilities

**File:** `skills/web-security/deserialization/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Insecure Deserialization
Skill. Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Insecure Deserialization Interface](interface.md).

---

# Capability Model

```
Authorization

Serialized Probing

Out-Of-Band Analysis

Differential Analysis

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

# Serialized Probing Capabilities

## Bounded Serialized Probing

The skill SHALL submit bounded, non-destructive serialized probes through the
[HTTP Client](../../shared/http-client/README.md).

---

# Out-Of-Band Analysis Capabilities

## Interaction Analysis

The skill SHALL determine whether an out-of-band interaction to a controlled collector
confirms unsafe deserialization.

---

# Differential Analysis Capabilities

## Differential Analysis

The skill SHALL determine whether response or timing differentials indicate
serialized-object processing, using the canonical
[HTTP Timing](../../../schemas/http-timing.md) representation.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify insecure deserialization weaknesses from observed behavior
and classify them using canonical weakness identifiers such as CWE-502.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only bounded probe interaction
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
- Test other injection classes
- Deliver a functional gadget chain or execute code
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Serialized Probing | Serialized Probing | SHALL |
| Interaction Analysis | Out-Of-Band Analysis | SHALL |
| Differential Analysis | Differential Analysis | SHALL |
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
- [HTTP Timing Schema](../../../schemas/http-timing.md)
