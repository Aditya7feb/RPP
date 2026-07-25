# Skill Error Handling

**File:** `skills/core/error-handling.md`

**Version:** 1.0.0

---

# Purpose

The Skill Error Handling specification defines how skills detect, classify, report, recover from, and propagate errors within the Robust PenTest Platform (RPP).

A standardized error model enables consistent orchestration, retry behavior, observability, debugging, auditing, and reporting.

Errors SHALL be treated as structured runtime events rather than implementation-specific exceptions.

---

# Design Principles

Errors SHALL be

- Structured
- Deterministic
- Traceable
- Actionable
- Recoverable where possible
- Auditable
- Platform Independent

A skill SHALL never silently ignore an error.

---

# Relationship

```
Skill

↓

Execution

↓

Error

↓

Agent Response

↓

Execution State

↓

Master Agent
```

Errors SHALL propagate through the canonical schemas.

---

# Error Philosophy

Errors represent

- Failed execution
- Unexpected runtime conditions
- Policy violations
- Invalid configuration
- Environmental failures

Errors SHALL describe

- What happened
- Why it happened
- Where it happened
- Whether recovery is possible
- Recommended next action

---

# Error Structure

Every error SHALL define

```yaml
error_id:

timestamp:

category:

severity:

component:

message:

details:

recoverable:
```

---

# Error Categories

Supported categories include

```
Validation

Configuration

Authentication

Authorization

Dependency

Network

Timeout

Resource

Environment

Execution

Capability

Tool

Policy

Internal

Unknown
```

Additional categories MAY be introduced.

---

# Error Severity

Supported values

```
Info

Warning

Error

Critical
```

Severity describes operational impact.

Severity SHALL NOT determine retry behavior.

---

# Recoverability

Errors SHALL indicate recoverability.

Supported values

```
Recoverable

Non-Recoverable

Unknown
```

Examples

Recoverable

- DNS timeout
- Temporary network issue
- Rate limiting
- Service unavailable

Non-Recoverable

- Invalid target
- Missing required input
- Unsupported capability
- Invalid configuration

---

# Error Sources

Errors MAY originate from

- Skill implementation
- Runtime environment
- External tools
- Network
- Target system
- Execution engine
- Policy engine

The source SHOULD be recorded.

---

# Execution Phase

Every error SHOULD identify the lifecycle phase.

Examples

```
Initialization

Validation

Preparation

Execution

Evidence Collection

Result Generation

Cleanup
```

---

# Context

Errors SHOULD include execution context.

```yaml
assessment_id:

task_id:

skill:

target:

execution_id:
```

This information improves troubleshooting and auditing.

---

# Root Cause

Errors SHOULD distinguish

```yaml
symptom:

root_cause:

impact:
```

Example

```
Symptom

Connection refused

↓

Root Cause

Target service unavailable
```

---

# Retry Guidance

Every recoverable error SHOULD define

```yaml
retry_recommended:

maximum_attempts:

backoff_strategy:

retry_after:
```

Supported backoff strategies

```
Constant

Linear

Exponential
```

The Master Agent SHALL determine whether retries are performed.

---

# Error Propagation

Errors SHALL be returned through the Agent Response schema.

Errors SHALL NOT terminate the entire assessment unless explicitly required.

Dependent tasks MAY be skipped based on policy.

---

# Partial Success

Skills MAY complete with recoverable errors.

Example

```
100 Hosts

↓

95 Successful

↓

5 Timeout
```

The skill SHALL return

```
Status

↓

Partial Success
```

Previously collected evidence SHALL be preserved.

---

# External Tool Failures

When external tools fail

The error SHOULD include

```yaml
tool:

version:

exit_code:

stderr:

stdout:
```

The original tool output SHOULD be preserved when possible.

---

# Policy Violations

Policy-related errors include

- Scope violation
- Approval missing
- Rate limit exceeded
- Restricted target
- Unsafe capability

Policy violations SHALL stop execution immediately.

---

# Dependency Failures

If a mandatory dependency fails

The skill SHALL

- Record the dependency
- Record the reason
- Return a structured error
- Skip execution

Optional dependency failures MAY allow execution to continue.

---

# Evidence Preservation

Errors SHALL NOT discard collected evidence.

Examples

- HTTP Requests
- HTTP Responses
- Screenshots
- Certificates
- Logs

Previously collected evidence SHALL remain available.

---

# Cleanup Errors

Cleanup failures SHALL be reported independently.

Cleanup failures SHALL NOT overwrite the original execution error.

Multiple errors MAY exist for a single execution.

---

# Error Metrics

Implementations SHOULD record

```yaml
total_errors:

recoverable_errors:

critical_errors:

retry_count:
```

Metrics SHOULD support operational monitoring.

---

# Audit Requirements

Every error SHALL be auditable.

Audit information SHOULD include

```yaml
reported_by:

reported_at:

platform_version:

skill_version:
```

---

# Validation Rules

A compliant error SHALL define

- Error ID
- Category
- Severity
- Message
- Recoverability
- Timestamp
- Execution Context

---

# Quality Requirements

The error model SHALL

✓ Produce structured errors

✓ Preserve execution context

✓ Preserve evidence

✓ Support retries

✓ Support auditing

✓ Support partial success

✓ Support policy enforcement

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY include

- Error correlation
- Distributed tracing
- Automatic remediation
- AI-assisted diagnostics
- Error fingerprints
- Incident integration

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Error Handling model provides a consistent mechanism for identifying, classifying, reporting, and recovering from execution failures.

It enables every skill within the Robust PenTest Platform to communicate failures predictably while preserving evidence, maintaining observability, and supporting resilient orchestration.