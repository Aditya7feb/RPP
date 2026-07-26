# Insecure Direct Object Reference Capabilities

**File:** `skills/web-security/idor/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Insecure Direct Object
Reference Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Insecure Direct Object Reference Interface](interface.md).

---

# Capability Model

```
Authorization

Reference Probing

Authorization Analysis

Cross-Identity Analysis

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

# Reference Probing Capabilities

## Controlled Reference Probing

The skill SHALL request object references using authorized controlled identities
through the [HTTP Client](../../shared/http-client/README.md).

---

# Authorization Analysis Capabilities

## Per-Object Authorization Analysis

The skill SHALL determine whether per-object authorization is enforced on referenced
objects.

---

# Cross-Identity Analysis Capabilities

## Cross-Identity Access Analysis

The skill SHALL determine whether one controlled identity can access another
controlled identity's object.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify IDOR weaknesses from observed behavior and classify them
using canonical weakness identifiers such as CWE-639.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only minimal controlled
confirmation recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including references tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test authentication mechanisms
- Enumerate or exfiltrate other principals' data
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Controlled Reference Probing | Reference Probing | SHALL |
| Per-Object Authorization Analysis | Authorization Analysis | SHALL |
| Cross-Identity Access Analysis | Cross-Identity Analysis | SHALL |
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
