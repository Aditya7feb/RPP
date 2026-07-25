# Workflow Runtime Execution Model

**File:** `skills/shared/workflow-runtime/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Workflow Runtime Shared Skill.

The execution model describes how the shared skill drives a resolved
[Execution Plan](../../../schemas/execution-plan.md) from loading through
scheduling, gating, dispatch, and finalization.

The model is deterministic given the same plan, inputs, and skill outcomes.

---

# Execution Overview

```
Load Execution Plan

↓

Resolve Configuration

↓

Validate Dependency Graph

↓

Initialize Execution State

↓

Scheduling Loop

↓

Finalize

↓

Return Execution Result
```

---

# Stage 1 — Plan Loading

The Workflow Runtime SHALL load the resolved
[Execution Plan](../../../schemas/execution-plan.md) referenced by the
invocation.

A plan derived from a
[Workflow Definition](../../../schemas/workflow-definition.md) SHALL already be
resolved to concrete steps.

---

# Stage 2 — Configuration Resolution

The Workflow Runtime SHALL resolve scheduling, approvals, default policies, and
state settings using the precedence defined in [configuration.md](configuration.md).

Approval enforcement SHALL always be active.

---

# Stage 3 — Dependency Validation

The Workflow Runtime SHALL build the step dependency graph and SHALL reject the
plan if the graph is cyclic or references undefined dependencies.

---

# Stage 4 — State Initialization

The Workflow Runtime SHALL initialize canonical
[Execution State](../../../schemas/execution-state.md), marking all steps
`pending`.

On resume, the runtime SHALL load durable state and restore completed steps.

---

# Stage 5 — Scheduling Loop

```
Select Ready Steps (dependencies satisfied)

↓

For Each Ready Step:

  ├── Evaluate condition
  │     └── false → mark skipped
  ├── Evaluate for_each
  ├── Enforce approval gate
  │     └── not granted → mark gated, emit ApprovalRequired
  ├── Apply policies (rate-limit, retry, proxy)
  ├── Dispatch to skill capability
  ├── Record normalized outcome
  └── Apply on_error behavior on failure

↓

Update State

↓

Repeat Until No Ready Steps Remain
```

Independent ready steps MAY be dispatched concurrently, bounded by
`max_concurrency`.

---

# Stage 6 — Approval Enforcement

A gated step SHALL NOT dispatch until its referenced
[Approval](../../../schemas/approval.md) is granted.

When a gate blocks progress and no other steps are ready, the runtime SHALL
return `awaiting_approval` with the pending gates and durable state.

---

# Stage 7 — Policy Application

At dispatch, the Workflow Runtime SHALL apply the step's

- [Rate Limit Policy](../../../schemas/rate-limit-policy.md) via the
  [Rate Limiter](../rate-limiter/README.md)
- [Retry Policy](../../../schemas/retry-policy.md) via the
  [Retry](../retry/README.md) shared skill
- [Proxy Configuration](../../../schemas/proxy-configuration.md) via the
  [Proxy](../proxy/README.md) shared skill

Steps without explicit policies SHALL inherit configured defaults.

---

# Stage 8 — Step Dispatch

The Workflow Runtime SHALL dispatch the step to the referenced skill capability
through its canonical interface, passing bound parameters and prior outputs.

The runtime SHALL record the normalized outcome and any produced finding and
evidence references without interpreting them.

---

# Stage 9 — Error Behavior

On step failure the runtime SHALL apply `on_error`

- `fail` terminates the workflow as `failed`
- `continue` marks the step failed and proceeds with independent steps
- `skip_remaining` skips dependent steps and proceeds to finalization

---

# Stage 10 — Finalization

When no reachable steps remain schedulable, the Workflow Runtime SHALL finalize,
emit outputs, and return the terminal outcome and state reference.

---

# Determinism

Given identical plan, inputs, and skill outcomes, scheduling order and terminal
state SHALL be identical apart from timestamps and references.

Concurrency SHALL NOT alter terminal state, only timing.

---

# Resumability

Under durable state, the runtime SHALL resume from the last checkpoint.

Completed idempotent steps SHALL NOT be re-executed. Non-idempotent steps SHALL
NOT be re-executed unless declared safe.

---

# Interaction With Other Shared Skills

- The [Rate Limiter](../rate-limiter/README.md), [Retry](../retry/README.md),
  and [Proxy](../proxy/README.md) shared skills govern step traffic.
- The [Evidence](../evidence/README.md) shared package stores evidence produced
  by steps.
- The [Reporting](../reporting/README.md) shared package consumes findings after
  execution.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

Runtime failures SHALL preserve durable state so that the workflow MAY be
resumed or audited.

---

# Execution Outputs

The execution model SHALL produce

- Final [Execution State](../../../schemas/execution-state.md)
- Step outcome summaries
- Workflow metrics
- Finding and evidence references produced by steps

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Execution Plan Schema](../../../schemas/execution-plan.md)
- [Execution State Schema](../../../schemas/execution-state.md)
- [Execution Model](../../core/execution-model.md)
