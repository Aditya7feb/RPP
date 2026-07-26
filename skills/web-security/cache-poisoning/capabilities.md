# Web Cache Poisoning Capabilities

**File:** `skills/web-security/cache-poisoning/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Web Cache Poisoning Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Web Cache Poisoning Interface](interface.md).

---

# Capability Model

```
Authorization

Cache Probing

Unkeyed Input Analysis

Cache Reflection Analysis

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

The skill SHALL test only in-scope applications.

---

# Cache Probing Capabilities

## Controlled Cache-Key Probing

The skill SHALL submit bounded probes against a controlled cache key through the
[HTTP Client](../../shared/http-client/README.md).

---

# Unkeyed Input Analysis Capabilities

## Unkeyed Input Analysis

The skill SHALL determine whether request inputs that influence responses are excluded
from the cache key.

---

# Cache Reflection Analysis Capabilities

## Cache Reflection Analysis

The skill SHALL determine whether an unkeyed input is reflected into a cached response
under a controlled cache key.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify cache poisoning weaknesses from observed behavior and classify
them using canonical weakness identifiers such as CWE-444.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only controlled-cache-key
confirmation recorded.

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
- Test script execution in cached responses
- Poison a cache entry that serves real users
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Controlled Cache-Key Probing | Cache Probing | SHALL |
| Unkeyed Input Analysis | Unkeyed Input Analysis | SHALL |
| Cache Reflection Analysis | Cache Reflection Analysis | SHALL |
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
- [HTTP Header Schema](../../../schemas/http-header.md)
