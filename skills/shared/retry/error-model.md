# Retry Error Model

**File:** `skills/shared/retry/error-model.md`

**Version:** 1.0.0

---

# Purpose

The Retry Error Model defines how failures related to retry orchestration are
classified, normalized, reported, and recovered within the Robust PenTest
Platform (RPP).

It extends the platform-wide error framework defined in
[the platform error handling model](../../core/error-handling.md).

This document distinguishes two concerns:

- Errors produced by the *operation* being retried, which the Retry Shared Skill
  classifies and propagates.
- Errors produced by the *retry orchestration itself*, which the Retry Shared
  Skill owns.

---

# Design Principles

Errors SHALL be

- Deterministic
- Structured
- Bounded
- Observable
- Evidence-backed
- Implementation Independent

---

# Error Lifecycle

```
Failure Occurs

↓

Detect

↓

Classify

↓

Normalize

↓

Capture Evidence

↓

Determine Recovery

↓

Publish Event

↓

Return Canonical Error
```

---

# Error Categories

The Retry Shared Skill SHALL classify orchestration errors into one of the
following categories.

| Category | Description |
|----------|-------------|
| Configuration | Invalid or unresolved retry configuration or policy |
| Validation | Invalid invocation before the first attempt |
| Budget | Attempt or elapsed-time budget exhausted |
| Deadline | Execution deadline reached before success |
| Aborted | Terminal abort category encountered |
| Idempotency | Retry blocked by idempotency constraints |
| Cancelled | Execution cancelled by the platform |
| Internal | Unexpected Retry Shared Skill failure |

Operation errors retain their original canonical category and are propagated
unchanged on the terminal attempt.

---

# Canonical Error Structure

Every Retry Shared Skill error SHALL expose

```yaml
error_id:

category:

code:

message:

severity:

recoverable:

retryable:

timestamp:

request_id:

policy_id:

terminal_outcome:

evidence:
```

---

# Configuration Errors

Examples include

- Referenced policy cannot be resolved
- Policy violates a global bound
- Invalid backoff strategy
- Missing default policy

When `fail_closed` is enabled, unresolved policies SHALL raise a configuration
error rather than silently disabling retries.

---

# Validation Errors

Examples include

- Missing operation reference
- Invalid inline policy override
- Deadline in the past
- Attempt override raising the budget

Validation errors SHALL prevent the first attempt.

---

# Budget Errors

Raised when retries are exhausted.

The terminal outcome SHALL be `exhausted`.

The error SHALL indicate the limiting bound, such as `max_attempts` or
`max_elapsed_time`, and SHALL propagate the last operation error.

---

# Deadline Errors

Raised when the execution deadline would be exceeded by a further attempt.

The terminal outcome SHALL be `deadline_exceeded`.

Deadline enforcement SHALL take precedence over the attempt budget.

---

# Aborted Errors

Raised when the operation returns an error whose category appears in the policy
`abort_on` list.

The terminal outcome SHALL be `aborted`.

No further attempts SHALL be scheduled.

---

# Idempotency Errors

Raised when a policy sets `idempotent_only` and the operation is not declared
idempotent.

The Retry Shared Skill SHALL NOT retry, and SHALL propagate the operation error
on the single attempt.

---

# Cancelled Errors

Raised when the platform cancels execution.

Collected evidence SHALL be preserved and resources SHALL be released.

---

# Internal Errors

Unexpected failures within the Retry Shared Skill.

Examples include

- Backoff computation failure
- State corruption
- Unexpected exception

Internal implementation details SHALL NOT be exposed to callers.

---

# Operation Error Propagation

The Retry Shared Skill SHALL preserve the last canonical operation error when a
retry loop terminates without success.

The propagated error SHALL retain its original category, code, and evidence, and
SHALL be wrapped with retry metadata including attempt count and terminal
outcome.

---

# Error Severity

| Severity | Meaning |
|----------|---------|
| Low | Retry succeeded after transient failures |
| Medium | Retry exhausted but recovery may be possible elsewhere |
| High | Operation failed terminally |
| Critical | Orchestration entered an unsafe or corrupt state |

---

# Retry Guidance

Retry orchestration errors are generally terminal and SHALL NOT themselves be
retried by the caller. In particular

- Configuration errors SHALL NOT be retried
- Validation errors SHALL NOT be retried
- Budget and Deadline errors indicate exhaustion and SHALL NOT be retried

Callers MAY escalate to alternate strategies such as a different transport,
session refresh, or graceful termination.

---

# Evidence Requirements

Errors SHOULD preserve

- Policy reference
- Attempt history
- Delays applied
- Elapsed time
- Terminal outcome
- Last operation error

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Observability

The Retry Shared Skill SHOULD emit events including

- RetryExhausted
- RetryAborted
- RetryDeadlineExceeded
- RetryConfigurationError
- RetryCancelled

Events SHALL integrate with the platform Execution State.

---

# Logging

Logs SHOULD include

```yaml
request_id:

assessment_id:

task_id:

policy_id:

terminal_outcome:

attempt_count:
```

Sensitive information SHALL be redacted.

---

# Recovery Expectations

Recovery MAY include

- Escalation to an alternate transport
- Session or authentication refresh
- Reduced scope
- Graceful termination

Recovery SHALL follow platform policy.

---

# Validation Rules

A compliant Retry error model SHALL

- Produce canonical errors
- Preserve the last operation error
- Distinguish orchestration errors from operation errors
- Preserve evidence
- Emit observable events
- Avoid exposing implementation details

---

# Quality Requirements

The error model SHALL

✓ Classify orchestration failures deterministically

✓ Preserve operation errors

✓ Preserve evidence

✓ Integrate with platform error handling

✓ Remain operation independent

✓ Support observability

✓ Protect sensitive information

---

# Future Extensions

Future versions MAY include

- Circuit-breaker error categories
- Aggregated batch error reporting
- Adaptive recovery recommendations

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry Error Model provides a consistent mechanism for representing
both retry-orchestration failures and propagated operation failures.

It enables reliable escalation, standardized reporting, and evidence
preservation while maintaining interoperability with the platform-wide error
handling framework.
