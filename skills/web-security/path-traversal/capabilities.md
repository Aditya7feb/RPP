# Path Traversal Capabilities

**File:** `skills/web-security/path-traversal/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Path Traversal Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Path Traversal Interface](interface.md).

---

# Capability Model

```
Authorization

Traversal Probing

Canonicalization Analysis

Marker Read Analysis

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

# Traversal Probing Capabilities

## Bounded Traversal Probing

The skill SHALL inject bounded traversal probes through the
[HTTP Client](../../shared/http-client/README.md).

---

## Encoding Bypass Probing

The skill SHALL probe encoded and double-encoded traversal sequences.

---

# Canonicalization Analysis Capabilities

## Canonicalization Analysis

The skill SHALL determine whether path input is safely canonicalized before use.

---

# Marker Read Analysis Capabilities

## Marker Read Confirmation

The skill SHALL confirm traversal by reading a non-sensitive marker resource outside
the intended base directory.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify path traversal weaknesses from observed behavior and classify
them using canonical weakness identifiers such as CWE-22.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only non-sensitive marker reads
recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including path parameters tested and findings
emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test SSRF or file upload
- Read, exfiltrate, or modify sensitive files
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Bounded Traversal Probing | Traversal Probing | SHALL |
| Encoding Bypass Probing | Traversal Probing | SHALL |
| Canonicalization Analysis | Canonicalization Analysis | SHALL |
| Marker Read Confirmation | Marker Read Analysis | SHALL |
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
