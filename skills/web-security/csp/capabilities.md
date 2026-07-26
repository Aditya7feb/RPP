# Content Security Policy Capabilities

**File:** `skills/web-security/csp/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Content Security Policy
Skill. Capabilities describe *what* the skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Content Security Policy Interface](interface.md).

---

# Capability Model

```
Authorization

Policy Observation

Directive Analysis

Source Strength Analysis

Bypass Analysis

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

# Policy Observation Capabilities

## Header And Meta Observation

The skill SHALL observe the `Content-Security-Policy` header and meta policy through
the [HTTP Client](../../shared/http-client/README.md).

---

## Enforcement Mode Observation

The skill SHALL observe whether the policy is enforcing or report-only.

---

# Directive Analysis Capabilities

## Directive Coverage Analysis

The skill SHALL analyze whether key directives such as `script-src`, `object-src`,
and `base-uri` are present.

---

# Source Strength Analysis Capabilities

## Unsafe Source Analysis

The skill SHALL determine whether `unsafe-inline` or `unsafe-eval` is permitted.

---

## Broad Source Analysis

The skill SHALL determine whether wildcard or overly broad sources neutralize the
policy.

---

# Bypass Analysis Capabilities

## Known Bypass Analysis

The skill SHALL determine whether allow-listed hosts or schemes enable known
bypasses.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify CSP weaknesses from observed policy and classify them using
canonical weakness identifiers such as CWE-693.

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
- Test for script execution
- Perform destructive exploitation
- Produce a Finding without Evidence
- Act on out-of-scope applications

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Header And Meta Observation | Policy Observation | SHALL |
| Enforcement Mode Observation | Policy Observation | SHALL |
| Directive Coverage Analysis | Directive Analysis | SHALL |
| Unsafe Source Analysis | Source Strength Analysis | SHALL |
| Broad Source Analysis | Source Strength Analysis | SHALL |
| Known Bypass Analysis | Bypass Analysis | SHALL |
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
