# Open Redirect Capabilities

**File:** `skills/web-security/open-redirect/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Open Redirect Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Open Redirect Interface](interface.md).

---

# Capability Model

```
Authorization

Redirect Observation

Parameter Analysis

Destination Analysis

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

# Redirect Observation Capabilities

## Redirect Response Observation

The skill SHALL observe redirect responses through the
[HTTP Client](../../shared/http-client/README.md).

---

# Parameter Analysis Capabilities

## Redirect Parameter Analysis

The skill SHALL identify user-controllable parameters that determine redirect
targets.

---

# Destination Analysis Capabilities

## Destination Validation Analysis

The skill SHALL determine whether redirect destinations are validated against an
allow-list of trusted origins.

---

## Untrusted Origin Analysis

The skill SHALL determine whether redirection to an untrusted external origin is
accepted, using a benign controlled destination.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify open-redirect weaknesses from observed behavior and classify
them using canonical weakness identifiers such as CWE-601.

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

The skill SHOULD expose metrics including checks performed and findings emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test SSRF or script execution
- Follow a redirect into a harmful destination
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Redirect Response Observation | Redirect Observation | SHALL |
| Redirect Parameter Analysis | Parameter Analysis | SHALL |
| Destination Validation Analysis | Destination Analysis | SHALL |
| Untrusted Origin Analysis | Destination Analysis | SHALL |
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
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
