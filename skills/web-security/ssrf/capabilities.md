# Server-Side Request Forgery Capabilities

**File:** `skills/web-security/ssrf/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Server-Side Request Forgery
Skill. Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Server-Side Request Forgery Interface](interface.md).

---

# Capability Model

```
Authorization

Request Probing

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

# Request Probing Capabilities

## Controlled Destination Probing

The skill SHALL submit bounded probes toward a controlled destination through the
[HTTP Client](../../shared/http-client/README.md).

---

# Out-Of-Band Analysis Capabilities

## Interaction Analysis

The skill SHALL determine whether an out-of-band interaction to a controlled collector
confirms server-side request forgery.

---

# Differential Analysis Capabilities

## Response Differential Analysis

The skill SHALL determine whether response or timing differentials indicate a
server-side fetch, using the canonical
[HTTP Timing](../../../schemas/http-timing.md) representation.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify SSRF weaknesses from observed behavior and classify them
using canonical weakness identifiers such as CWE-918.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only controlled-destination
interaction recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including parameters tested and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test client-side redirection
- Reach internal services, cloud metadata, or sensitive endpoints
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Controlled Destination Probing | Request Probing | SHALL |
| Interaction Analysis | Out-Of-Band Analysis | SHALL |
| Response Differential Analysis | Differential Analysis | SHALL |
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
