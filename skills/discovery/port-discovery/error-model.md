# Port Discovery Error Model

**File:** `skills/discovery/port-discovery/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Port Discovery Skill.

The error model classifies the failure conditions the skill MAY produce and
aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Port Discovery Skill SHALL

- Produce canonical, structured errors
- Treat Policy Engine denial as a normal outcome, not a fault
- Continue probing other ports when one fails
- Never produce a Finding without Evidence

---

# Error Categories

The skill maps its failures onto the canonical categories.

```
Configuration

Validation

Authorization

Probe

Analysis

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Invalid default protocol
- Non-positive bounds

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing target
- Missing scope or Rules-of-Engagement references
- Unbounded port range without explicit configuration

Validation errors SHALL be non-retryable.

---

# Authorization Errors

Raised in relation to Policy Engine decisions.

A `deny` decision SHALL produce a `denied` outcome recorded as evidence, not an
error.

The skill SHALL NOT probe when authorization is absent.

---

# Probe Errors

Raised when a port cannot be probed.

Probe errors SHALL propagate the canonical
[TCP Client](../../shared/tcp-client/README.md) or
[UDP Client](../../shared/udp-client/README.md) error, SHALL be recorded, and
SHALL NOT abort probing of other ports.

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

port:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the probe MAY be attempted again.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| denied | Authorization (normal outcome) | No |
| probe_failed | Probe | Per client policy |
| analysis_failed | Analysis | No |
| invalid_request | Validation | No |
| invalid_config | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Partial-Result Principle

A failure affecting one port SHALL NOT abort the discovery. The overall outcome
SHALL be `partial` when some probes did not complete, and produced objects SHALL
remain valid and evidence-backed.

---

# Evidence

Errors and denials SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, target,
and port, and SHALL exclude secrets.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [TCP Client](../../shared/tcp-client/README.md)
