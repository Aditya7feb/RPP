# Workflow Runtime Error Model

**File:** `skills/shared/workflow-runtime/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Workflow Runtime Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Workflow Runtime Shared Skill SHALL

- Produce canonical, structured errors
- Distinguish step failures from runtime failures
- Preserve durable state on failure to support resumption and audit
- Never bypass approval gates on error

---

# Error Categories

The Workflow Runtime maps its failures onto the canonical categories.

```
Configuration

Validation

Scheduling

Approval

Policy

Dispatch

State

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- `max_concurrency` less than `1`
- Approval enforcement disabled
- A referenced default policy does not exist
- `resumable` set without durable state

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when a plan or invocation is malformed.

Conditions

- Cyclic dependency graph
- A step referencing an undefined dependency
- A step referencing a tool or implementation
- Missing plan reference

Validation errors SHALL be non-retryable.

---

# Scheduling Errors

Raised when scheduling cannot proceed.

Conditions

- Deadlock caused by unsatisfiable dependencies
- Workflow timeout exceeded

Scheduling errors SHALL preserve state and SHALL be surfaced for diagnosis.

---

# Approval Errors

Raised when an approval gate cannot be satisfied.

Conditions

- A required approval is denied
- A gate references a missing approval requirement

A denied approval SHALL terminate the gated branch without dispatching the
intrusive step. Approval errors SHALL NOT be bypassed.

---

# Policy Errors

Raised when a required policy cannot be applied.

Conditions

- A referenced policy cannot be resolved
- A Rules of Engagement ceiling would be violated

Policy errors SHALL prevent dispatch of the affected step.

---

# Dispatch Errors

Raised when a step cannot be dispatched or the skill returns an error.

Dispatch errors SHALL be handled per the step `on_error` behavior.

A skill error propagated as `on_error: fail` SHALL terminate the workflow.

---

# State Errors

Raised when execution state cannot be persisted or loaded.

State errors under durable configuration SHALL be surfaced, since they threaten
resumability.

---

# Adapter Errors

Raised when an underlying state or coordination mechanism fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Workflow Runtime.

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

step_id:

state_ref:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| approvals_disabled | Configuration | No |
| cyclic_plan | Validation | No |
| tool_reference | Validation | No |
| deadlock | Scheduling | No |
| workflow_timeout | Scheduling | No |
| approval_denied | Approval | No |
| policy_unresolved | Policy | No |
| roe_violation | Policy | No |
| step_failed | Dispatch | Per on_error |
| state_persist_failed | State | Policy dependent |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# State Preservation Principle

On any runtime failure, the Workflow Runtime SHALL preserve durable state
sufficient to resume or audit the workflow.

A failure SHALL NOT leave the workflow in an unrecoverable or unauditable state.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Execution State Schema](../../../schemas/execution-state.md)
- [Approval Schema](../../../schemas/approval.md)
