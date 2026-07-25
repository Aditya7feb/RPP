# Recon Execution Model

**File:** `skills/discovery/recon/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Recon Skill, stage
by stage. Given the same Scope, configuration, and composed-skill outputs,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Build Workflow Definition

↓

Authorize And Run Passive Phase

↓

Approval Gate (active phase)

↓

Authorize And Run Active Phase

↓

Consolidate Asset Graph (Asset Discovery)

↓

Aggregate Findings And Evidence

↓

Return Consolidated Result
```

Recon performs no probing at any stage.

---

# Stage 1 — Validate Request

The skill SHALL validate that `scope_id`, `roe_id`, and `targets` are present and
well formed and that every composed skill exists. Invalid requests SHALL fail
closed.

---

# Stage 2 — Build Workflow Definition

The skill SHALL construct a
[Workflow Definition](../../../schemas/workflow-definition.md) that orders the
selected Discovery skills into a passive phase and an active phase, with an
approval gate before the active phase.

---

# Stage 3 — Authorize And Run Passive Phase

The skill SHALL request phase authorization from the
[Policy Engine](../../shared/policy-engine/README.md). On authorization it SHALL
drive the passive Discovery skills through the
[Workflow Runtime](../../shared/workflow-runtime/README.md). Passive skills gather
information without target-facing intrusion, subject to their own policy checks.

---

# Stage 4 — Approval Gate

Before the active phase the skill SHALL evaluate the approval gate. Where the
Policy Engine decision is `requires_approval`, the skill SHALL pause the workflow
and return `awaiting_approval` until approval is granted through the platform
approval flow. The active phase SHALL NOT begin until the gate is satisfied.

---

# Stage 5 — Authorize And Run Active Phase

On approval the skill SHALL request active-phase authorization and drive the active
Discovery skills through the Workflow Runtime. Each active skill enforces policy on
every action and honors its own rate ceiling.

---

# Stage 6 — Consolidate Asset Graph

The skill SHALL invoke [Asset Discovery](../asset-discovery/README.md) with the
Assets, Relationships, and Evidence produced by the composed skills to obtain a
deduplicated, scope-confirmed asset graph.

---

# Stage 7 — Aggregate Findings And Evidence

The skill SHALL aggregate [Findings](../../../schemas/finding.md),
[Observations](../../../schemas/observation.md), and
[Evidence](../../../schemas/evidence.md) from all composed skills, preserving each
Finding's supporting Evidence.

---

# Stage 8 — Return Consolidated Result

The skill SHALL return the consolidated Assets, relationships, aggregated findings,
observations, evidence, the executed workflow reference, a `status`, and metrics
per the [interface](interface.md).

---

# Determinism Guarantees

- Same Scope, configuration, and skill outputs yield the same result.
- Phase order and approval gates are fixed by the Workflow Definition.
- Consolidation is delegated to Asset Discovery, not performed inline.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). A denied phase halts
per configuration. A failed skill step yields partial results with aggregated
Evidence where `continue_on_step_error` is enabled. Pending approvals yield
`awaiting_approval`.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Workflow Runtime Execution](../../shared/workflow-runtime/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
