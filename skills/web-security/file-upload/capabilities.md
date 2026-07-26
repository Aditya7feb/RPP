# Unrestricted File Upload Capabilities

**File:** `skills/web-security/file-upload/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Unrestricted File Upload
Skill. Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Unrestricted File Upload Interface](interface.md).

---

# Capability Model

```
Authorization

Upload Probing

Type Validation Analysis

Content Validation Analysis

Storage Exposure Analysis

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

# Upload Probing Capabilities

## Inert Marker Upload

The skill SHALL submit inert, non-executable marker files through the
[HTTP Client](../../shared/http-client/README.md).

---

# Type Validation Analysis Capabilities

## Type Validation Analysis

The skill SHALL determine whether file-type validation is adequate or based only on
extension or client-supplied content type.

---

# Content Validation Analysis Capabilities

## Content Validation Analysis

The skill SHALL determine whether file content is validated beyond declared type.

---

# Storage Exposure Analysis Capabilities

## Storage Exposure Analysis

The skill SHALL determine whether uploaded content is stored in a web-accessible
location or served with an unsafe content type.

---

# Weakness Analysis Capabilities

## Weakness Identification

The skill SHALL identify file upload weaknesses from observed behavior and classify
them using canonical weakness identifiers such as CWE-434.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md), each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) with only inert marker uploads
recorded.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including upload endpoints tested and findings
emitted.

---

# Capability Boundaries

The skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints
- Test path traversal
- Upload or execute functional malicious payloads
- Produce a Finding without Evidence
- Act on out-of-scope targets

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Consultation | Authorization | SHALL |
| Scope Confinement | Authorization | SHALL |
| Inert Marker Upload | Upload Probing | SHALL |
| Type Validation Analysis | Type Validation Analysis | SHALL |
| Content Validation Analysis | Content Validation Analysis | SHALL |
| Storage Exposure Analysis | Storage Exposure Analysis | SHALL |
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
