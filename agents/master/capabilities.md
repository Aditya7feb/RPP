# Master Agent Capabilities

**File:** `agents/master/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the orchestration capabilities owned by the Master
Agent. Every capability listed here is a **coordination** capability. None
performs security analysis, produces Findings, collects Evidence, or scores
Risk.

---

# Capability Summary

| ID | Capability | Decides | Canonical binding |
|----|------------|---------|-------------------|
| MA-C1 | Planning | WHAT work is required, and in what order | `execution-plan` |
| MA-C2 | Reasoning | WHY each action is justified | `execution-state` |
| MA-C3 | Delegation | WHO performs each unit of work | `task` |
| MA-C4 | Workflow coordination | WHICH reusable sequence applies | `workflow-definition` |
| MA-C5 | Approval gating | WHETHER a gated action may proceed | `approval` |
| MA-C6 | Execution tracking | WHERE the assessment currently stands | `execution-state` |
| MA-C7 | Completion | WHEN the assessment is finished | `assessment` |

---

# MA-C1 — Planning

The Master Agent SHALL convert an assessment request into an
[execution-plan](../../schemas/execution-plan.md).

Planning SHALL:

- Validate that scope, RoE, and target are present and supported.
- Determine mandatory and optional work.
- Order work by dependency, scope, expected confidence gain, and cost.
- Identify which capability tiers apply to the target class.
- Insert approval gates before any intrusive or state-changing validation.

Planning SHALL NOT execute work; it only produces the plan.

---

# MA-C2 — Reasoning

Before every action the Master Agent SHALL justify it against current, non-stale
[execution-state](../../schemas/execution-state.md).

Reasoning SHALL separate **facts** (supported by referenced Evidence) from
**assumptions** (not supported by Evidence). Assumptions SHALL never be treated
as Findings; deriving Findings is a capability responsibility.

The reasoning cycle — Observe, Understand, Reason, Plan, Delegate, Review,
Reflect — is defined in [execution.md](execution.md).

---

# MA-C3 — Delegation

The Master Agent SHALL delegate every unit of work to the specialist tier agent
that owns the required capability, expressed as a [task](../../schemas/task.md).

Delegation SHALL:

- Match required capability to the owning capability tier.
- Target capabilities, never tools.
- Validate dependencies are satisfied before dispatch.
- Assign exactly one primary owner per task.

The delegation contract and capability-to-tier routing are defined in
[interface.md](interface.md).

---

# MA-C4 — Workflow Coordination

The Master Agent SHALL sequence reusable, domain-specific work using
[workflow-definition](../../schemas/workflow-definition.md) objects (for example,
the web-app, rest-api, graphql, and wordpress workflows). Workflow coordination
selects and orders workflows; it does not embed capability logic.

---

# MA-C5 — Approval Gating

The Master Agent SHALL pause the assessment and obtain explicit human
authorization before any intrusive, state-changing, or high-risk action, using
an [approval](../../schemas/approval.md) object. Approval requirements apply
regardless of confidence.

Gating configuration and the actions that require approval are defined in
[configuration.md](configuration.md).

---

# MA-C6 — Execution Tracking

The Master Agent SHALL maintain
[execution-state](../../schemas/execution-state.md) reflecting planned, running,
completed, and failed work, and the current assessment phase. Tracking is the
authoritative record of orchestration progress.

---

# MA-C7 — Completion

The Master Agent SHALL determine assessment completion when all mandatory phases
have completed, no runnable work remains, approvals are resolved, and the
reporting pipeline has produced its outputs. Completion finalizes the
[assessment](../../schemas/assessment.md), referencing produced content by
identifier.

---

# Capability Boundaries

The following are explicitly **outside** every Master Agent capability and are
owned by capability tiers: producing Findings, collecting or promoting Evidence,
assigning Risk, deduplicating or correlating results, computing presentation
figures, and defining confidence. See [README.md](README.md) for the ownership
table.
