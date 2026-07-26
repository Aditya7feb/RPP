# SQL Injection Capabilities

**File:** `skills/web-security/sqli/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the SQL Injection Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[SQL Injection Interface](interface.md).

---

# Capability Model

```
Authorization

Injection Probing

Error Signal Analysis

Boolean Signal Analysis

Time Signal Analysis

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

# Injection Probing Capabilities

## Bounded Probe Injection

The skill SHALL inject bounded, non-destructive probes through the
[HTTP Client](../../shared/http-client/README.md).

---

# Error Signal Analysis Capabilities

## Error Signal Analysis

The skill SHALL determine whether malformed input yields database error signals.

---

# Boolean Signal Analysis Capabilities

## Boolean Divergence Analysis

The skill SHALL determine whether true and false conditions produce divergent
responses.

---

# Time Signal Analysis Capabilities

## Time Delay Analysis

The skill SHALL determine whether a bounded, induced delay confirms blind injection,
using the canonical [HTTP Timing](../../../schemas/http-timing.md) representation.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify SQL injection weaknesses from observed signals and classify
them using canonical weakness identifiers such as CWE-89.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with the confirming signal recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including injection points tested and findings
emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test other injection classes
- Extract, modify, or destroy data
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Probe Injection | Injection Probing | SHALL |
| Error Signal Analysis | Error Signal Analysis | SHALL |
| Boolean Divergence Analysis | Boolean Signal Analysis | SHALL |
| Time Delay Analysis | Time Signal Analysis | SHALL |
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
