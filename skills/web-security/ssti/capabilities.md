# Server-Side Template Injection Capabilities

**File:** `skills/web-security/ssti/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Server-Side Template
Injection Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Server-Side Template Injection Interface](interface.md).

---

# Capability Model

```
Authorization

Injection Probing

Evaluation Analysis

Engine Indication Analysis

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

## Bounded Marker Injection

The skill SHALL inject bounded, non-destructive expression markers through the
[HTTP Client](../../shared/http-client/README.md).

---

# Evaluation Analysis Capabilities

## Expression Evaluation Analysis

The skill SHALL determine whether a bounded expression marker is evaluated by the
server.

---

# Engine Indication Analysis Capabilities

## Engine Class Analysis

The skill SHALL determine which template engine class is indicated by evaluation
behavior, informing exploitability.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify template injection weaknesses from observed behavior and
classify them using canonical weakness identifiers such as CWE-1336.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with the evaluated marker recorded.

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
- Test client-side injection or other injection classes
- Escalate to code execution or run system commands
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Marker Injection | Injection Probing | SHALL |
| Expression Evaluation Analysis | Evaluation Analysis | SHALL |
| Engine Class Analysis | Engine Indication Analysis | SHALL |
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
