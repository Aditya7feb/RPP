# GraphQL API Security Capabilities

**File:** `skills/api-security/graphql/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the GraphQL API Security Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[GraphQL API Security Interface](interface.md).

---

# Capability Model

```
Authorization

Query Probing

Introspection Analysis

Depth And Complexity Analysis

Field Authorization Analysis

Batching Analysis

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

# Query Probing Capabilities

## Bounded Query Probing

The skill SHALL submit bounded GraphQL queries using authorized controlled identities
through the [HTTP Client](../../shared/http-client/README.md).

---

# Introspection Analysis Capabilities

## Introspection Analysis

The skill SHALL determine whether introspection is enabled and discloses the schema.

---

# Depth And Complexity Analysis Capabilities

## Depth And Complexity Analysis

The skill SHALL determine whether query depth and complexity limits are enforced,
using bounded probes.

---

# Field Authorization Analysis Capabilities

## Field Authorization Analysis

The skill SHALL determine whether field- and object-level authorization is enforced
across identities.

---

# Batching Analysis Capabilities

## Batching Analysis

The skill SHALL determine whether batching or alias-based amplification is constrained.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify GraphQL security weaknesses from observed behavior and
classify them using canonical identifiers and OWASP API Security Top 10 (2023)
references.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only bounded, minimal
confirmation recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including queries tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover APIs or endpoints
- Test generic injection or client-side weaknesses
- Execute unbounded depth or complexity queries
- Enumerate or exfiltrate other principals' data
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Query Probing | Query Probing | SHALL |
| Introspection Analysis | Introspection Analysis | SHALL |
| Depth And Complexity Analysis | Depth And Complexity Analysis | SHALL |
| Field Authorization Analysis | Field Authorization Analysis | SHALL |
| Batching Analysis | Batching Analysis | SHALL |
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
