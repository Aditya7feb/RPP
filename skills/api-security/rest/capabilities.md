# REST API Security Capabilities

**File:** `skills/api-security/rest/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the REST API Security Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[REST API Security Interface](interface.md).

---

# Capability Model

```
Authorization

Operation Probing

Object Authorization Analysis

Function Authorization Analysis

Property Authorization Analysis

Resource Consumption Analysis

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

# Operation Probing Capabilities

## Controlled Operation Probing

The skill SHALL exercise REST operations using authorized controlled identities
through the [HTTP Client](../../shared/http-client/README.md).

---

# Object Authorization Analysis Capabilities

## Object Level Authorization Analysis

The skill SHALL determine whether object level authorization is enforced across
identities.

---

# Function Authorization Analysis Capabilities

## Function Level Authorization Analysis

The skill SHALL determine whether privileged functions enforce function level
authorization.

---

# Property Authorization Analysis Capabilities

## Mass Assignment Analysis

The skill SHALL determine whether protected properties can be modified through mass
assignment.

---

## Excessive Data Exposure Analysis

The skill SHALL determine whether responses expose more data than the caller requires.

---

# Resource Consumption Analysis Capabilities

## Resource Consumption Analysis

The skill SHALL determine whether pagination and rate limiting constrain resource
consumption.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify API security weaknesses from observed behavior and classify
them using canonical identifiers and OWASP API Security Top 10 (2023) references.

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

The skill SHOULD expose metrics including operations tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints
- Test generic injection or client-side weaknesses
- Enumerate or exfiltrate other principals' data
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Controlled Operation Probing | Operation Probing | SHALL |
| Object Level Authorization Analysis | Object Authorization Analysis | SHALL |
| Function Level Authorization Analysis | Function Authorization Analysis | SHALL |
| Mass Assignment Analysis | Property Authorization Analysis | SHALL |
| Excessive Data Exposure Analysis | Property Authorization Analysis | SHALL |
| Resource Consumption Analysis | Resource Consumption Analysis | SHALL |
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
