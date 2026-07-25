# Rate Limiter Error Model

**File:** `skills/shared/rate-limiter/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Rate Limiter Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Rate Limiter SHALL

- Produce canonical, structured errors
- Distinguish caller errors from governance rejections
- Preserve enough context for auditing
- Avoid leaking secrets or implementation detail

---

# Error Categories

The Rate Limiter maps its failures onto the canonical categories.

```
Configuration

Validation

RateLimited

Governance

Timeout

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid or incomplete.

Conditions

- `default_policy_id` references a missing policy
- A policy reference does not resolve
- A required scope input is absent for the policy `scope`

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing operation callback
- Invalid inline policy override
- Priority is not an integer

Validation errors SHALL be non-retryable.

---

# Rate Limited Errors

Raised when an operation cannot proceed under the resolved policy.

Conditions

- `on_limit.action` is `reject` and no permit is available
- Queue depth would exceed `max_queue_depth`
- Wait exceeds `max_wait`

Rate-limited errors SHALL indicate whether the caller MAY retry later and SHOULD
include the recommended earliest retry time when known.

---

# Governance Errors

Raised when an operation would violate a Rules of Engagement ceiling.

Conditions

- A resolved policy or override exceeds an enforced ceiling
- An operation targets a scope suppressed by a `Retry-After` signal beyond its
  deadline

Governance errors SHALL be non-retryable without operator intervention.

---

# Timeout Errors

Raised when a permit cannot be acquired before a deadline.

Conditions

- `deadline` elapses while queued
- `max_wait` elapses while queued

Timeout errors SHALL carry the elapsed wait time.

---

# Adapter Errors

Raised when an underlying coordination mechanism fails, such as a distributed
permit store becoming unavailable.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

Adapter errors MAY be retryable depending on the caller policy.

---

# Internal Errors

Raised for unexpected conditions within the Rate Limiter.

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

scope_key:

policy_id:

earliest_retry:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

`earliest_retry`, when present, SHALL indicate the earliest time a retry MAY
succeed.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| rejected | RateLimited | Yes, later |
| shed | RateLimited | Yes, later |
| deadline_exceeded | Timeout | No |
| ceiling_exceeded | Governance | No |
| invalid_invocation | Validation | No |
| missing_policy | Configuration | No |
| coordination_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Interaction With Retry

A `RateLimited` error indicates the operation may succeed later. When combined
with [Retry](../retry/README.md), such errors MAY be retried subject to the
retry policy, and each retry SHALL acquire a fresh permit.

A `Governance` error SHALL NOT be retried automatically.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, scope
key, and policy reference.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
- [Retry](../retry/README.md)
