# DNS Enumeration Error Model

**File:** `skills/discovery/dns-enumeration/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the DNS Enumeration Skill.

The error model classifies the failure conditions the skill MAY produce and
aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The DNS Enumeration Skill SHALL

- Produce canonical, structured errors
- Treat Policy Engine denial as a normal outcome, not a fault
- Continue enumerating other names when one fails
- Never produce a Finding without Evidence

---

# Error Categories

The skill maps its failures onto the canonical categories.

```
Configuration

Validation

Authorization

Resolution

Analysis

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Unrecognized default record type
- Non-positive bounds

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing target
- Missing scope or Rules-of-Engagement references

Validation errors SHALL be non-retryable.

---

# Authorization Errors

Raised in relation to Policy Engine decisions.

A `deny` decision SHALL produce a `denied` outcome recorded as evidence, not an
error. A malformed policy request SHALL be a validation error.

The skill SHALL NOT act when authorization is absent.

---

# Resolution Errors

Raised when the DNS Client cannot resolve a name.

Resolution errors SHALL propagate the canonical
[DNS Client](../../shared/dns-client/README.md) error, SHALL be recorded, and
SHALL NOT abort enumeration of other names.

---

# Analysis Errors

Raised when weakness analysis cannot complete.

Analysis errors SHALL NOT fabricate Findings and SHALL be surfaced for
diagnosis; enumeration results remain valid.

---

# Adapter Errors

Raised when an underlying shared package fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the skill.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

target:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the action MAY be attempted again.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| denied | Authorization (normal outcome) | No |
| resolution_failed | Resolution | Per DNS Client policy |
| analysis_failed | Analysis | No |
| invalid_request | Validation | No |
| invalid_config | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Partial-Result Principle

A failure affecting one name SHALL NOT abort the enumeration. The overall outcome
SHALL be `partial` when some planned actions did not complete, and produced
objects SHALL remain valid and evidence-backed.

---

# Evidence

Errors and denials SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category and
target, and SHALL exclude secrets.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [DNS Client](../../shared/dns-client/README.md)
