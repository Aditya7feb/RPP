# Workflow Runtime Shared Skill

**File:** `skills/shared/workflow-runtime/README.md`

**Version:** 1.0.0

---

# Purpose

The Workflow Runtime Shared Skill provides the canonical,
implementation-independent engine that executes assessment workflows within the
Robust PenTest Platform (RPP).

Rather than allowing each workflow or agent to implement its own orchestration,
this shared skill centralizes step scheduling, dependency resolution, control
flow, approval gating, policy application, state management, and workflow
observability.

All workflow execution SHALL be driven through this shared skill.

---

# Goals

The Workflow Runtime Shared Skill SHALL

- Execute a resolved [Execution Plan](../../../schemas/execution-plan.md)
  derived from a [Workflow Definition](../../../schemas/workflow-definition.md)
- Resolve step dependencies and schedule execution
- Evaluate declarative control flow
- Enforce approval gates before intrusive steps
- Apply execution policies to steps
- Maintain canonical [Execution State](../../../schemas/execution-state.md)
- Delegate step execution to skills without embedding skill logic
- Integrate with platform observability

---

# Non-Goals

The Workflow Runtime Shared Skill SHALL NOT

- Implement domain skill logic
- Detect vulnerabilities
- Produce findings itself
- Perform target-facing operations directly
- Decide approvals; it SHALL enforce them
- Compose reports

The Workflow Runtime *orchestrates* skills. Skills perform the work; the runtime
sequences it.

---

# Design Principles

The Workflow Runtime Shared Skill SHALL be

- Deterministic given the same plan, inputs, and skill outcomes
- Dependency aware
- Policy driven
- Resumable
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Workflow Runtime Shared Skill

├── Plan Loader
├── Dependency Scheduler
├── Control Flow Evaluator
├── Approval Gatekeeper
├── Policy Applier
├── Step Dispatcher
├── State Manager
├── Event Manager

↓

Domain and Shared Skills
```

The Workflow Runtime dispatches steps to skills through their canonical
interfaces. It SHALL remain unaware of skill implementations.

---

# Responsibilities

The Workflow Runtime Shared Skill is responsible for

- Loading a resolved [Execution Plan](../../../schemas/execution-plan.md)
- Building the step dependency graph
- Scheduling ready steps
- Evaluating conditions, iteration, and error behavior
- Enforcing [Approval](../../../schemas/approval.md) gates
- Applying rate-limit, retry, and proxy policies to steps
- Dispatching steps to skills
- Updating [Execution State](../../../schemas/execution-state.md)
- Emitting workflow lifecycle events

---

# Execution Lifecycle

```
Load Execution Plan

↓

Build Dependency Graph

↓

Initialize Execution State

↓

Loop:

  ├── Select Ready Steps
  ├── Evaluate Conditions
  ├── Enforce Approval Gates
  ├── Apply Policies
  ├── Dispatch To Skill
  ├── Record Outcome
  └── Update State

↓

Finalize And Emit Outputs
```

Execution SHALL continue until all reachable steps reach a terminal state.

---

# Dependency Scheduling

The Workflow Runtime SHALL schedule a step only after all steps in its
`depends_on` have completed successfully, subject to `on_error` behavior.

The dependency graph SHALL be acyclic. A cyclic plan SHALL be rejected before
execution.

Independent ready steps MAY be dispatched concurrently.

---

# Control Flow

The Workflow Runtime SHALL evaluate declarative control flow defined in the
[Workflow Definition schema](../../../schemas/workflow-definition.md)

- `condition` gates step execution
- `for_each` iterates a step over a collection
- `on_error` determines behavior on step failure

Control-flow predicates SHALL be side-effect free.

---

# Approval Gates

The Workflow Runtime SHALL enforce approval gates before intrusive steps.

A gated step SHALL NOT dispatch until the referenced
[Approval](../../../schemas/approval.md) is granted.

The runtime enforces, but SHALL NOT decide, approvals. Approval decisions belong
to the approval process of the Master Agent.

---

# Policy Application

The Workflow Runtime SHALL apply the execution policies referenced by a step or
plan, including

- [Rate Limit Policy](../../../schemas/rate-limit-policy.md) through the
  [Rate Limiter](../rate-limiter/README.md)
- [Retry Policy](../../../schemas/retry-policy.md) through the
  [Retry](../retry/README.md) shared skill
- [Proxy Configuration](../../../schemas/proxy-configuration.md) through the
  [Proxy](../proxy/README.md) shared skill

Policies SHALL be applied at dispatch so that all step traffic remains governed.

---

# State Management

The Workflow Runtime SHALL maintain canonical
[Execution State](../../../schemas/execution-state.md) recording step status,
outcomes, and timing.

State SHALL be durable enough to support resumption after interruption.

---

# Resumability

The Workflow Runtime SHOULD support resuming an interrupted execution from the
last durable state without re-running completed idempotent steps.

Non-idempotent steps SHALL NOT be re-executed on resume unless explicitly
declared safe.

---

# Step Dispatch

The Workflow Runtime SHALL dispatch a step to the referenced skill capability
through the skill's canonical interface.

The runtime SHALL pass bound parameters and prior step outputs and SHALL record
the normalized outcome.

The runtime SHALL NOT inspect or embed skill implementation.

---

# Events

The Workflow Runtime SHOULD publish

- WorkflowStarted
- StepScheduled
- StepStarted
- ApprovalRequired
- StepCompleted
- StepFailed
- WorkflowCompleted
- WorkflowResumed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Workflow Runtime Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Execution Plan Schema](../../../schemas/execution-plan.md)
- [Execution State Schema](../../../schemas/execution-state.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
- [Approval Schema](../../../schemas/approval.md)
- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Proxy](../proxy/README.md)

The Workflow Runtime SHALL orchestrate domain skills without depending on any
specific one.

---

# Consumers

Typical consumers include

- The Master Agent
- Domain workflows under `workflows/`
- Assessment execution processes

---

# Outputs

Typical outputs MAY include

- Final execution state
- Aggregated step outcomes
- Workflow metrics
- Evidence and finding references produced by steps

Outputs SHALL remain implementation independent.

---

# Security Principles

The Workflow Runtime Shared Skill SHALL

- Enforce approval gates before intrusive actions
- Apply rate-limit and proxy policies to all step traffic
- Preserve Rules of Engagement across the workflow
- Protect secrets in parameter bindings
- Preserve an auditable execution trail

Orchestration without gating could cause unauthorized intrusive actions. The
runtime SHALL enforce authorization boundaries at every gate.

---

# Best Practices

Consumers SHOULD

- Express reusable procedures as workflow definitions
- Place approval gates before intrusive steps
- Reference shared policies rather than inlining values
- Declare step idempotency for safe resumption
- Rely on the runtime for scheduling and state

---

# Anti-Patterns

Consumers SHOULD NOT

- Orchestrate steps outside the runtime
- Bypass approval gates
- Embed skill logic in workflow definitions
- Reference tools or implementations in steps
- Re-run non-idempotent steps on resume

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-workflow-runtime-abstraction.md

---

# Related Shared Packages

- [Rate Limiter](../rate-limiter/README.md)
- [Retry](../retry/README.md)
- [Proxy](../proxy/README.md)
- [Evidence](../evidence/README.md)
- [Reporting](../reporting/README.md)

---

# Canonical Schemas

- [Workflow Definition](../../../schemas/workflow-definition.md)
- [Execution Plan](../../../schemas/execution-plan.md)
- [Execution State](../../../schemas/execution-state.md)
- [Approval](../../../schemas/approval.md)

---

# Architecture Decisions

- [ADR-001 — Workflow Runtime Abstraction](adr/ADR-001-workflow-runtime-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Parallel branch fan-out and join semantics
- Sub-workflow composition
- Compensation and rollback steps
- Distributed multi-worker execution

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Workflow Runtime Shared Skill provides a deterministic, resumable,
and implementation-independent orchestration engine for the Robust PenTest
Platform.

It enables consistent execution of reusable workflows across every domain while
enforcing approvals and policies and preserving an auditable execution trail,
without embedding skill logic.
