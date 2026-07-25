# Workflow Runtime Capabilities

**File:** `skills/shared/workflow-runtime/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Workflow Runtime Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Workflow Runtime Interface](interface.md).

---

# Capability Model

```
Plan Loading

Scheduling

Control Flow

Approval Enforcement

Policy Application

Dispatch

State Management

Observability
```

---

# Plan Loading Capabilities

## Plan Loading

The Workflow Runtime SHALL load a resolved
[Execution Plan](../../../schemas/execution-plan.md).

---

## Plan Validation

The Workflow Runtime SHALL reject a plan whose dependency graph is cyclic or
whose steps reference undefined dependencies.

---

# Scheduling Capabilities

## Dependency Resolution

The Workflow Runtime SHALL schedule a step only after its dependencies complete.

---

## Concurrent Dispatch

The Workflow Runtime MAY dispatch independent ready steps concurrently.

---

# Control Flow Capabilities

## Conditional Execution

The Workflow Runtime SHALL evaluate step `condition` predicates.

---

## Iteration

The Workflow Runtime SHALL evaluate `for_each` iteration over collections.

---

## Error Behavior

The Workflow Runtime SHALL apply `on_error` behavior of `fail`, `continue`, or
`skip_remaining`.

---

# Approval Enforcement Capabilities

## Gate Enforcement

The Workflow Runtime SHALL block a gated step until its referenced
[Approval](../../../schemas/approval.md) is granted.

---

## Enforce Not Decide

The Workflow Runtime SHALL enforce approvals but SHALL NOT decide them.

---

# Policy Application Capabilities

## Rate And Proxy Policy

The Workflow Runtime SHALL apply rate-limit and proxy policies to step traffic
through the [Rate Limiter](../rate-limiter/README.md) and
[Proxy](../proxy/README.md) shared skills.

---

## Retry Policy

The Workflow Runtime SHALL apply retry policies through the
[Retry](../retry/README.md) shared skill.

---

# Dispatch Capabilities

## Skill Dispatch

The Workflow Runtime SHALL dispatch steps to skill capabilities through their
canonical interfaces.

---

## Parameter Binding

The Workflow Runtime SHALL bind workflow parameters and prior step outputs to
step invocations.

---

# State Management Capabilities

## State Maintenance

The Workflow Runtime SHALL maintain canonical
[Execution State](../../../schemas/execution-state.md).

---

## Resumption

The Workflow Runtime SHOULD resume interrupted executions from durable state
without re-running completed idempotent steps.

---

# Observability Capabilities

## Event Emission

The Workflow Runtime SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The Workflow Runtime SHOULD expose metrics including steps scheduled, completed,
failed, and gated.

---

# Capability Boundaries

The Workflow Runtime SHALL NOT

- Implement skill logic
- Produce findings
- Decide approvals
- Reference tools or implementations
- Perform target-facing operations directly

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Plan Loading | Plan Loading | SHALL |
| Plan Validation | Plan Loading | SHALL |
| Dependency Resolution | Scheduling | SHALL |
| Concurrent Dispatch | Scheduling | MAY |
| Conditional Execution | Control Flow | SHALL |
| Iteration | Control Flow | SHALL |
| Error Behavior | Control Flow | SHALL |
| Gate Enforcement | Approval | SHALL |
| Enforce Not Decide | Approval | SHALL |
| Rate And Proxy Policy | Policy | SHALL |
| Retry Policy | Policy | SHALL |
| Skill Dispatch | Dispatch | SHALL |
| Parameter Binding | Dispatch | SHALL |
| State Maintenance | State | SHALL |
| Resumption | State | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
