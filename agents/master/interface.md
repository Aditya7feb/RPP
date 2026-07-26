# Master Agent Interface

**File:** `agents/master/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent contract through
which the Master Agent delegates work to specialist tier agents and consumes
their results. The contract is transport-independent: it applies whether agents
communicate via message queues, local calls, remote procedure calls, or future
mechanisms.

---

# Design Principles

Every interaction SHALL be structured, deterministic, versioned, idempotent,
traceable, and observable. The transport mechanism SHALL NOT affect the
contract.

---

# Delegation Contract

The Master Agent issues work as a [task](../../schemas/task.md) and receives an
[agent-response](../../schemas/agent-response.md).

```yaml
task:                     # canonical task object
  capability:             # required capability (not a tool)
  target:                 # in-scope target reference
  scope_ref:              # references scope
  roe_ref:                # references rules-of-engagement
  approval_ref:           # references approval when the task is gated
  inputs:                 # explicit inputs (references only)
```

```yaml
agent-response:           # canonical agent-response object
  task_ref:               # the task this responds to
  status:                 # completed | failed | rejected | partial
  observation_refs:       # references to observations produced
  evidence_refs:          # references to evidence produced
  finding_refs:           # references to findings produced
  next_recommended:       # optional suggested follow-on capabilities
```

The Master Agent SHALL consume only **references** from an agent-response. It
SHALL NOT copy, merge, or mutate the referenced Findings, Evidence, or
Observations.

---

# Capability Routing

The Master Agent routes each required capability to the specialist tier agent
that owns it. Routing targets capability tiers, never tools.

| Capability domain | Specialist tier agent | Capability tier |
|-------------------|----------------------|-----------------|
| Attack-surface discovery | Discovery Agent | [skills/discovery](../../skills/discovery/README.md) |
| Identity and session analysis | Authentication Agent | [skills/authentication](../../skills/authentication/README.md) |
| Web application security | Web Security Agent | [skills/web-security](../../skills/web-security/README.md) |
| API security | API Security Agent | [skills/api-security](../../skills/api-security/README.md) |
| Cloud posture | Cloud Agent | [skills/cloud](../../skills/cloud/README.md) |
| Payload-driven active testing | Active Testing Agent | [skills/active-testing](../../skills/active-testing/README.md) |
| Evidence capture and correlation | Evidence Agent | [skills/evidence](../../skills/evidence/README.md) |
| Result presentation | Reporting Agent | [skills/reporting](../../skills/reporting/README.md) |

Each specialist tier agent coordinates the capability packages within its tier.
The Master Agent does not address individual packages; packages are
implementation details inside each capability tier.

---

# Communication Lifecycle

```text
Plan → Create task → Dispatch to specialist tier agent →
Specialist executes tier capabilities → agent-response returned →
execution-state updated → next task
```

---

# Roles

## Master Agent

Creates tasks, schedules work, tracks execution, enforces gates, receives
responses, and updates orchestration state. It SHALL NOT execute capability
logic.

## Specialist Tier Agent

Accepts tasks, coordinates the capability packages within its tier, and returns
structured `agent-response` objects with references to produced content.
Specialist tier agents SHALL NOT modify orchestration state directly.

---

# Approval Interaction

When a task is gated, the Master Agent SHALL create an
[approval](../../schemas/approval.md) request, pause the dependent task, and
dispatch it only after the approval reaches an approved state. Rejected or
expired approvals SHALL cause the assessment to stop at identification.

---

# Versioning

The task and agent-response contracts follow the versioning rules of their
canonical schemas. Unknown optional fields SHALL be ignored for forward
compatibility.
