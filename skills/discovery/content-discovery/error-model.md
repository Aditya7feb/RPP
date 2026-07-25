# Content Discovery Error Model

**File:** `skills/discovery/content-discovery/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Content Discovery Skill.

The error model classifies the failure conditions the skill MAY produce and
aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Content Discovery Skill SHALL

- Produce canonical, structured errors
- Treat Policy Engine denial as a normal outcome, not a fault
- Continue probing other paths when one fails
- Never produce a Finding without Evidence

---

# Error Categories

The skill maps its failures onto the canonical categories.

```
Configuration

Validation

Authorization

Request

Analysis

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Missing default wordlist
- `same_scope_only` disabled
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
error.

The skill SHALL NOT probe when authorization is absent.

---

# Request Errors

Raised when a path cannot be probed.

Request errors SHALL propagate the canonical
[HTTP Client](../../shared/http-client/README.md) error, SHALL be recorded, and
SHALL NOT abort probing of other paths.

---

# Analysis Errors

Raised when exposure analysis cannot complete.

Analysis errors SHALL NOT fabricate Findings and SHALL be surfaced for
diagnosis; probe results remain valid.

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

path:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the request MAY be attempted again.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| denied | Authorization (normal outcome) | No |
| request_failed | Request | Per HTTP Client policy |
| analysis_failed | Analysis | No |
| invalid_request | Validation | No |
| invalid_config | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Partial-Result Principle

A failure affecting one path SHALL NOT abort the discovery. The overall outcome
SHALL be `partial` when some requests did not complete, and produced objects SHALL
remain valid and evidence-backed.

---

# Evidence

Errors and denials SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, target,
and path, and SHALL exclude secrets.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [HTTP Client](../../shared/http-client/README.md)
