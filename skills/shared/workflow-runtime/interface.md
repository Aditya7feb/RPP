# Workflow Runtime Interface

**File:** `skills/shared/workflow-runtime/interface.md`

**Version:** 1.0.0

---

# Purpose

The Workflow Runtime Interface defines the canonical contract through which
platform components execute assessment workflows.

The interface standardizes plan submission, execution control, state
observation, and result propagation while remaining independent of any skill
implementation.

All workflow execution SHALL be driven through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Skill Independent
- Versioned
- Observable
- Backward Compatible
- Deterministic

---

# Relationship

```
Master Agent

↓

Workflow Runtime Interface

↓

Workflow Runtime Shared Skill

↓

Domain and Shared Skills
```

The interface SHALL NOT expose or depend on skill internals.

---

# Interface Overview

```
Metadata

↓

Plan Reference

↓

Inputs

↓

Execution Controls

↓

Execution Context

↓

Execution Result

↓

State Reference

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Plan Reference

Every invocation SHALL define

```yaml
execution_plan_id:
```

`execution_plan_id` SHALL reference a resolved
[Execution Plan](../../../schemas/execution-plan.md), typically instantiated
from a [Workflow Definition](../../../schemas/workflow-definition.md).

---

# Inputs

Every invocation SHALL define

```yaml
parameters:

target_ref:
```

`parameters` SHALL bind declared workflow parameters.

`parameters` SHALL NOT contain secrets; credentials SHALL be referenced
indirectly.

---

# Execution Controls

The caller MAY specify

```yaml
mode:

resume_from_state:

max_concurrency:
```

`mode` SHALL be one of `run`, `dry_run`, or `resume`.

`dry_run` SHALL validate and schedule without dispatching intrusive steps.

`resume_from_state` SHALL reference durable
[Execution State](../../../schemas/execution-state.md) to resume.

`max_concurrency` SHALL bound concurrent step dispatch.

---

# Execution Context

The Workflow Runtime Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Execution Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

state_ref:

step_summaries:

pending_approvals:

metrics:
```

`outcome` SHALL be one of

```
completed

failed

awaiting_approval

paused
```

`state_ref` SHALL reference the canonical
[Execution State](../../../schemas/execution-state.md).

`pending_approvals` SHALL list gates awaiting authorization when `outcome` is
`awaiting_approval`.

---

## Step Summary

Each step summary SHALL include

```yaml
step_id:

status:

skill:

capability:

started_at:

completed_at:
```

`status` SHALL be one of `pending`, `running`, `completed`, `failed`, `skipped`,
or `gated`.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Workflow Runtime error model](error-model.md).

A step failure SHALL be handled per its `on_error` behavior rather than
necessarily failing the workflow.

---

# Determinism

Given identical plan, inputs, and skill outcomes, the runtime SHALL produce
identical scheduling and terminal state apart from timestamps and references.

---

# Compatibility

The interface SHALL remain stable across skills and domains.

Consumers SHALL require no modification when skills change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Plan Reference
- Inputs
- Execution Context
- Execution Result

---

# Quality Requirements

The Workflow Runtime Interface SHALL

✓ Remain skill independent

✓ Produce canonical execution state

✓ Enforce approval gates

✓ Support structured errors

✓ Support resumption

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Branch fan-out and join descriptors
- Sub-workflow invocation
- Streaming step notifications

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Workflow Runtime Interface provides a stable,
implementation-independent contract through which all platform components execute
gated, policy-governed, resumable workflows across the Robust PenTest Platform.
