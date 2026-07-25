# ADR-001 — Workflow Runtime Abstraction

**File:** `skills/shared/workflow-runtime/adr/ADR-001-workflow-runtime-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform executes multi-step assessments composed of many
skill invocations with dependencies, conditions, approval gates, and governing
policies. Orchestration is a cross-cutting concern shared by every domain and
every workflow. It carries several requirements:

- Deterministic, dependency-aware scheduling
- Enforcement of approval gates before intrusive actions
- Consistent application of rate-limit, retry, and proxy policies
- Durable state and resumption after interruption
- An auditable execution trail

Before this decision, orchestration could be implemented ad hoc inside each
workflow or agent. That approach produced inconsistent scheduling, unreliable
approval enforcement, divergent policy application, and no reliable resumption.

The platform requires a single, canonical, implementation-independent engine to
execute workflows.

---

# Decision

The platform SHALL provide a dedicated Workflow Runtime shared skill that
centralizes assessment orchestration behind a stable interface.

The Workflow Runtime shared skill SHALL

- Execute a resolved
  [Execution Plan](../../../../schemas/execution-plan.md) derived from a
  reusable [Workflow Definition](../../../../schemas/workflow-definition.md)
- Resolve dependencies and schedule steps deterministically
- Evaluate declarative control flow
- Enforce [Approval](../../../../schemas/approval.md) gates before intrusive
  steps
- Apply rate-limit, retry, and proxy policies at dispatch
- Maintain durable
  [Execution State](../../../../schemas/execution-state.md) supporting resumption
- Dispatch steps to skills through their canonical interfaces

Consumers SHALL execute workflows exclusively through the
[Workflow Runtime Interface](../interface.md). The runtime SHALL orchestrate
skills without embedding skill logic and SHALL NOT reference tools or
implementations.

A reusable Workflow Definition schema is introduced as the declarative template,
distinct from the assessment-specific Execution Plan it is instantiated into and
the Execution State it produces.

---

# Alternatives Considered

## Ad Hoc Orchestration Per Workflow

Each workflow could orchestrate its own steps.

Rejected because it produces inconsistent scheduling, unreliable approval
enforcement, and no reliable resumption.

## Folding Orchestration Into The Master Agent

The Master Agent could orchestrate steps directly.

Rejected because orchestration is a reusable, testable engine distinct from
agent reasoning and planning. Separating the runtime keeps the agent focused on
decisions while the runtime focuses on execution mechanics.

## Reusing Execution Plan As The Template

The Execution Plan could serve as the reusable template.

Rejected because the Execution Plan is assessment-specific and resolved. A
distinct Workflow Definition provides a reusable, parameterized template that
planning instantiates into an Execution Plan, preserving a clean separation of
template, plan, and state.

---

# Consequences

## Positive

- Deterministic, dependency-aware scheduling across domains
- Reliable approval enforcement before intrusive actions
- Consistent policy application to all step traffic
- Durable state and resumption
- An auditable, reproducible execution trail

## Negative

- Consumers MUST execute workflows through the interface
- An additional shared dependency is introduced
- A new schema is added to the canonical set

The negative consequences are outweighed by the safety, consistency, and
auditability benefits.

---

# Compliance

Consumers SHALL

- Execute workflows through the Workflow Runtime Interface
- Express reusable procedures as Workflow Definitions
- Place approval gates before intrusive steps
- Reference shared policies rather than inlining values
- Declare step idempotency for safe resumption

The Workflow Runtime SHALL orchestrate skills without depending on any specific
domain skill, preserving downward-only dependencies.

---

# Future Compatibility

Future versions MAY introduce branch fan-out and join semantics, sub-workflow
composition, compensation steps, and distributed execution. These extensions
SHALL preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Workflow Runtime README](../README.md)
- [Workflow Runtime Interface](../interface.md)
- [Workflow Runtime Execution Model](../execution.md)
- [Workflow Runtime Error Model](../error-model.md)
- [Workflow Definition Schema](../../../../schemas/workflow-definition.md)
- [Execution Plan Schema](../../../../schemas/execution-plan.md)
- [Execution State Schema](../../../../schemas/execution-state.md)
- [Approval Schema](../../../../schemas/approval.md)
