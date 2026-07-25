# TLS Analysis Error Model

**File:** `skills/discovery/tls-analysis/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the TLS Analysis Skill.

The error model classifies the failure conditions the skill MAY produce and
aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The TLS Analysis Skill SHALL

- Produce canonical, structured errors
- Treat Policy Engine denial as a normal outcome, not a fault
- Distinguish a handshake failure from a weakness finding
- Never produce a Finding without Evidence

---

# Error Categories

The skill maps its failures onto the canonical categories.

```
Configuration

Validation

Authorization

Handshake

Analysis

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Unrecognized check or protocol threshold
- Interception boundary honoring disabled

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

The skill SHALL NOT analyze when authorization is absent.

---

# Handshake Errors

Raised when the TLS Client cannot complete a handshake.

A handshake failure SHALL be recorded as an Observation and MAY itself indicate a
posture issue; it SHALL NOT be fabricated into a weakness Finding without
Evidence.

Handshake errors SHALL propagate the canonical
[TLS Client](../../shared/tls-client/README.md) error.

---

# Analysis Errors

Raised when weakness analysis cannot complete.

Analysis errors SHALL NOT fabricate Findings and SHALL be surfaced for
diagnosis; analysis results remain valid.

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

`retryable` SHALL indicate whether the analysis MAY be attempted again.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| denied | Authorization (normal outcome) | No |
| handshake_failed | Handshake | Per TLS Client policy |
| analysis_failed | Analysis | No |
| invalid_request | Validation | No |
| invalid_config | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Interception Principle

A validation outcome caused by a legitimate interception boundary SHALL NOT be
treated as an error or a certificate weakness. The skill SHALL honor interception
boundaries reported by the TLS Client.

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
- [TLS Client](../../shared/tls-client/README.md)
