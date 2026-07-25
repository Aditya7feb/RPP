# Fingerprinting Error Model

**File:** `skills/discovery/fingerprinting/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Fingerprinting Skill.

The error model classifies the failure conditions the skill MAY produce and
aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Fingerprinting Skill SHALL

- Produce canonical, structured errors
- Treat Policy Engine denial as a normal outcome, not a fault
- Continue collecting other signals when one fails
- Never produce a Technology or Finding without Evidence

---

# Error Categories

The skill maps its failures onto the canonical categories.

```
Configuration

Validation

Authorization

Collection

Matching

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Unrecognized signal source
- Invalid minimum confidence

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

The skill SHALL NOT collect signals when authorization is absent.

---

# Collection Errors

Raised when a signal cannot be collected.

Collection errors SHALL propagate the canonical
[HTTP Client](../../shared/http-client/README.md) or
[TLS Client](../../shared/tls-client/README.md) error, SHALL be recorded, and
SHALL NOT abort collection of other signals.

---

# Matching Errors

Raised when technology matching cannot complete.

Matching errors SHALL NOT fabricate Technologies or Findings and SHALL be
surfaced for diagnosis; collected signals remain valid.

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
| collection_failed | Collection | Per client policy |
| matching_failed | Matching | No |
| invalid_request | Validation | No |
| invalid_config | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Confidence Principle

The skill SHALL grade identification confidence honestly and SHALL NOT record a
Technology below the configured minimum confidence.

Inferred identifications SHALL carry lower confidence than observed
identifications.

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
- [Technology Schema](../../../schemas/technology.md)
