# Master Agent Execution Model

**File:** `agents/master/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic, stage-by-stage execution model of the
Master Agent, including the reasoning cycle, the assessment lifecycle, the
reporting pipeline, and the memory model. Execution is orchestration only; no
stage performs capability business logic.

---

# Reasoning Cycle

Every decision follows a fixed cycle, repeated after each completed task.

```text
Observe → Understand → Reason → Plan → Delegate → Review → Reflect → (repeat)
```

- **Observe** — Load current, non-stale
  [execution-state](../../schemas/execution-state.md): phase, referenced
  Findings and Evidence, running and failed work, pending approvals, and RoE.
- **Understand** — Separate facts (Evidence-referenced) from assumptions.
- **Reason** — Justify the next action; if it cannot be justified, it SHALL NOT
  execute.
- **Plan** — Update or confirm the
  [execution-plan](../../schemas/execution-plan.md).
- **Delegate** — Issue a [task](../../schemas/task.md) to the owning specialist
  tier agent.
- **Review** — Record the returned
  [agent-response](../../schemas/agent-response.md) references.
- **Reflect** — Determine remaining work, avoiding duplication and out-of-scope
  actions.

---

# Assessment Lifecycle

```text
NEW
 ↓  validate input, load scope and RoE
PLANNING
 ↓  build execution plan and approval gates
DISCOVERY
 ↓  delegate to Discovery Agent; update target knowledge
CAPABILITY EXECUTION
 ↓  delegate to applicable tier agents (auth, web, api, cloud) in parallel
WAITING_APPROVAL
 ↓  gate intrusive validation; obtain approval
ACTIVE VALIDATION
 ↓  delegate to Active Testing Agent under approval
REPORTING
 ↓  drive the reporting pipeline
COMPLETED
```

Failure or cancellation transitions to `FAILED` or `CANCELLED`, preserving
execution state.

---

# Stage 1 — Intake and Planning

The Master Agent validates the [assessment](../../schemas/assessment.md),
[scope](../../schemas/scope.md), and
[rules-of-engagement](../../schemas/rules-of-engagement.md). If validation
fails, orchestration stops. On success it produces an
[execution-plan](../../schemas/execution-plan.md) with dependency ordering,
parallel groups, and inserted approval gates.

---

# Stage 2 — Discovery

The Master Agent delegates attack-surface discovery to the
[Discovery Agent](../discovery/README.md). Returned observations and asset
references update target knowledge, which informs which capability tiers apply.

---

# Stage 3 — Capability Execution

Based on target knowledge, the Master Agent delegates to the applicable
specialist tier agents — [Authentication](../authentication/README.md),
[Web Security](../web-security/README.md),
[API Security](../api-security/README.md), and [Cloud](../cloud/README.md) —
scheduling independent work in parallel where RoE permits. All produced Findings
and Evidence are owned by those tiers and referenced by identifier.

---

# Stage 4 — Approval and Active Validation

For each candidate that requires validation, the Master Agent creates an
[approval](../../schemas/approval.md) request and pauses the dependent task. Only
after approval does it delegate to the
[Active Testing Agent](../active-testing/README.md). Evidence produced during
validation is owned by the [Evidence Agent](../evidence/README.md) and the
Evidence tier.

---

# Stage 5 — Reporting Pipeline

The Master Agent drives the reporting pipeline by invoking Reporting capabilities
in order, consuming each output by reference. It performs none of this logic.

```text
delegate → finding-correlation   (deduplicate, relate, chain findings)
        ↓
delegate → risk-analysis         (aggregate, prioritize, presentation figures)
        ↓
delegate → report-generation     (executive/technical; SARIF/JSON/MD/PDF)
        ↓
delegate → evidence-bundle        (assemble referenced evidence)
```

Canonical Risk remains owned by the Domain Security tiers; risk-analysis produces
presentation figures only. See
[skills/reporting/README.md](../../skills/reporting/README.md).

---

# Stage 6 — Completion

When all mandatory phases are complete, no runnable work remains, approvals are
resolved, and reporting outputs exist, the Master Agent finalizes the
[assessment](../../schemas/assessment.md), referencing the produced Findings,
Evidence, Risk, and Reports by identifier.

---

# Quality Gates

Before each phase transition the Master Agent SHALL verify: execution state is
valid, the previous phase completed, required referenced inputs exist, no
blocking failures remain, and scope is maintained.

---

# Memory Model

- Memory and context exist **solely to support orchestration** — planning,
  sequencing, duplication avoidance, and reflection.
- **Capabilities remain deterministic.** No capability tier reads orchestration
  memory. A capability's output depends only on the explicit inputs of its
  [task](../../schemas/task.md).
- **Memory SHALL never become a hidden dependency.** Everything a capability
  needs — scope, RoE, and prior Evidence or Finding references — is passed
  explicitly in the task payload. Removing orchestration memory changes only
  orchestration efficiency and sequencing, never capability results.
- Context propagation is explicit: scope, RoE, and prior knowledge flow through
  task inputs and agent-response references, never through ambient state.

---

# Confidence

The Master Agent consumes confidence values to inform gating and scheduling but
does not define them. Confidence semantics are canonical and owned by
[skills/core/confidence-model.md](../../skills/core/confidence-model.md).
