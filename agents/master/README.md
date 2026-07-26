# Master Agent

**File:** `agents/master/README.md`

**Version:** 2.0.0

---

# Purpose

The Master Agent is the central **orchestrator** of the Robust PenTest Platform
(RPP). It converts an authorized assessment request into a coordinated sequence
of capability invocations, tracks their execution, enforces approval gates, and
determines when the assessment is complete.

The Master Agent is a **pure orchestrator**. It decides *what* should happen,
*who* should perform it, *when* it may proceed, and *whether* the assessment is
finished. It never performs the business logic of any capability. Findings,
Evidence, Risk, and Reporting outputs are produced exclusively by their owning
capability tiers and are consumed by the Master Agent **by reference only**.

---

# Goals

- Translate assessment intent into an ordered, dependency-aware execution plan.
- Delegate every unit of work to the capability tier that owns it.
- Enforce Rules of Engagement (RoE), scope, and human approval gates.
- Track execution state and phase transitions deterministically.
- Drive the reporting pipeline by invoking Reporting capabilities in order.
- Decide, on evidence, when the assessment is complete.

---

# Non-Goals

The Master Agent SHALL NOT:

- Execute tools, commands, or protocol clients directly.
- Create, modify, deduplicate, correlate, or prioritize Findings.
- Collect, package, promote, or mutate Evidence.
- Calculate or assign canonical Risk.
- Render reports or compute presentation figures.
- Define confidence semantics.

These responsibilities belong to the capability tiers and are enumerated as
explicit Non-Responsibilities below.

---

# Design Principles

- **Orchestration only.** The Master Agent reasons, plans, delegates, gates, and
  tracks. It owns coordination state, never capability state.
- **Capability-oriented.** All delegation targets **capabilities**, never tools.
  Work is routed to one of eight canonical capability tiers, each fronted by a
  specialist tier agent.
- **Schema-bound.** Every orchestration input, decision, and output is expressed
  through an existing canonical schema. The Master Agent introduces no schema.
- **Reference-based consumption.** Findings, Evidence, and Risk are immutable and
  are referenced by identifier; they are never copied or altered.
- **Determinism preserved.** Capabilities depend only on their declared task
  inputs. Orchestration memory never becomes a hidden capability input.
- **Human oversight.** Intrusive or state-changing validation SHALL pause for
  explicit human approval regardless of confidence.

---

# Architecture

```text
                 ┌───────────────────────────────────────────────┐
                 │                 Master Agent                  │
                 │  planning · reasoning · delegation ·          │
                 │  workflow coordination · approval gating ·    │
                 │  execution tracking · completion              │
                 └───────────────────────────────────────────────┘
                        │  delegates via task → agent-response
      ┌───────────┬─────┴────┬───────────┬───────────┬───────────┬───────────┬───────────┐
      ▼           ▼          ▼           ▼           ▼           ▼           ▼           ▼
 Discovery   Authentication  Web       API        Cloud      Active     Evidence   Reporting
   Agent        Agent      Security   Security     Agent     Testing      Agent      Agent
                            Agent      Agent                  Agent
      │           │          │           │           │           │           │           │
      ▼           ▼          ▼           ▼           ▼           ▼           ▼           ▼
  skills/discovery  skills/authentication  skills/web-security  …  skills/reporting
```

The Master Agent communicates with each specialist tier agent through the
canonical task contract. Each specialist tier agent coordinates the capability
packages within its own tier. Capability packages contain all domain business
logic and remain unaware of the orchestration layer.

---

# Responsibilities

The Master Agent SHALL own the following orchestration responsibilities.

| Responsibility | Description | Canonical binding |
|----------------|-------------|-------------------|
| Planning | Determine WHAT work is required and its order | `execution-plan` |
| Reasoning | Justify every action on current, non-stale state | `execution-state` |
| Delegation | Determine WHO performs each unit of work | `task` |
| Workflow coordination | Sequence reusable domain workflows | `workflow-definition` |
| Approval gating | Pause and resume around gated actions | `approval` |
| Execution tracking | Track progress, running, and failed work | `execution-state` |
| Completion | Decide when the assessment is finished | `assessment` |

---

# Explicit Non-Responsibilities

The Master Agent SHALL NOT own the following. Each is delegated to its owner.

| Responsibility | Owner |
|----------------|-------|
| Deduplicate, relate, or chain Findings | Reporting → finding-correlation |
| Aggregate, prioritize, normalize, or score Risk for presentation | Reporting → risk-analysis |
| Render executive/technical reports and serializations | Reporting → report-generation |
| Assemble Evidence into distributable bundles | Reporting → evidence-bundle |
| Collect, preserve, package, or promote Evidence | Evidence tier + shared evidence |
| Assign canonical Risk | Domain Security capability tiers |
| Define confidence semantics | Core → confidence-model |
| Execute tools or protocol operations | Capability tiers only |

---

# Inputs

The Master Agent receives an authorized assessment request expressed through
canonical schemas.

```yaml
assessment:            # canonical assessment object
  scope:               # references scope
  rules_of_engagement: # references rules-of-engagement
```

See [assessment](../../schemas/assessment.md), [scope](../../schemas/scope.md),
and [rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Outputs

The Master Agent produces orchestration artifacts only. All security content is
produced by capabilities and referenced here.

- An [execution-plan](../../schemas/execution-plan.md) describing planned work.
- Evolving [execution-state](../../schemas/execution-state.md) across the run.
- [approval](../../schemas/approval.md) requests at gated boundaries.
- A finalized [assessment](../../schemas/assessment.md) referencing the produced
  Findings, Evidence, Risk, and Reports by identifier.

---

# Assessment Lifecycle

```text
NEW → PLANNING → DISCOVERY → CAPABILITY EXECUTION →
WAITING_APPROVAL → ACTIVE VALIDATION → REPORTING → COMPLETED
                                   ↘ FAILED / CANCELLED
```

The deterministic, stage-by-stage execution model is defined in
[execution.md](execution.md).

---

# Dependencies

The Master Agent depends only on the eight specialist tier agents, each of which
fronts a canonical capability tier.

- [Discovery Agent](../discovery/README.md)
- [Authentication Agent](../authentication/README.md)
- [Web Security Agent](../web-security/README.md)
- [API Security Agent](../api-security/README.md)
- [Cloud Agent](../cloud/README.md)
- [Active Testing Agent](../active-testing/README.md)
- [Evidence Agent](../evidence/README.md)
- [Reporting Agent](../reporting/README.md)

The Master Agent references canonical schemas for all orchestration state and
references [skills/core/confidence-model.md](../../skills/core/confidence-model.md)
for confidence semantics. It defines none of these itself.

---

# Consumers

The Master Agent is the top of the orchestration hierarchy. No capability
package or schema depends on it. Human operators and external assessment
front-ends consume its outputs.

---

# Security Principles

- The Master Agent enforces scope, RoE, allowed hosts/ports/protocols,
  authentication boundaries, rate limits, excluded paths, and approval gates on
  every delegation. No specialist agent may bypass these controls.
- Intrusive or state-changing validation is never automatic; it requires an
  approved [approval](../../schemas/approval.md) object.
- Secrets are never emitted into orchestration state, logs, or references.

---

# Best Practices

- Delegate to capabilities; never inline capability logic.
- Reason before acting; never schedule work without justification on current
  state.
- Reuse existing Evidence and Findings by reference rather than re-requesting.
- Maximize safe parallelism only where dependencies and RoE permit.

---

# Anti-Patterns

- Performing finding deduplication, correlation, or risk scoring in the
  orchestration layer.
- Referencing tools, CLIs, or MCP operations from orchestration documents.
- Copying or mutating Findings, Evidence, or Risk.
- Treating orchestration memory as a capability input.

---

# Related Packages

- Specialist tier agents under `agents/` (the eight capability tiers).
- The Reporting tier at [skills/reporting/README.md](../../skills/reporting/README.md).
- The Evidence tier at [skills/evidence/README.md](../../skills/evidence/README.md).

---

# Canonical Schemas

[assessment](../../schemas/assessment.md),
[scope](../../schemas/scope.md),
[rules-of-engagement](../../schemas/rules-of-engagement.md),
[execution-plan](../../schemas/execution-plan.md),
[execution-state](../../schemas/execution-state.md),
[task](../../schemas/task.md),
[agent-response](../../schemas/agent-response.md),
[approval](../../schemas/approval.md),
[workflow-definition](../../schemas/workflow-definition.md).

---

# Architecture Decisions

- [ADR-001: Master Agent Architecture](adr/ADR-001-master-agent-architecture.md)

---

# Future Extensions

The Master Agent SHALL support discovery of additional capability tiers without
modification. Any compliant specialist tier agent that exposes a capability
registry and honors the task contract MAY participate in future assessments.

---

# Success Criteria

- Every delegated unit of work targets a capability tier, never a tool.
- No Finding, Evidence, or Risk logic executes in the orchestration layer.
- All orchestration state binds to an existing canonical schema.
- Confidence is referenced from Core, not redefined.
- Capabilities remain deterministic and independent of orchestration memory.
