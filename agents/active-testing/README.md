# Active Testing Agent

**File:** `agents/active-testing/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Active Testing Agent is the specialist tier agent that fronts the Active
Testing capability tier. It accepts delegated, **approval-gated** validation work
from the [Master Agent](../master/README.md), coordinates the capability packages
within [skills/active-testing](../../skills/active-testing/README.md), and returns
structured results by reference.

The Active Testing Agent is a thin coordinator. It contains no domain business
logic; all payload generation, mutation, replay, and validation logic lives in
the Active Testing capability packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the Active
  Testing tier and which carries an approved
  [approval](../../schemas/approval.md) reference.
- Select and order the Active Testing capability packages required to satisfy it.
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, validated findings, and evidence.

---

# Owned Capability Tier

[skills/active-testing](../../skills/active-testing/README.md) — payload-driven,
approval-gated validation, including fuzzing, replay, and validation payloads.

---

# Responsibilities

The Active Testing Agent SHALL:

- Require an approved approval reference on every task before coordinating any
  package.
- Coordinate intra-tier ordering of Active Testing packages.
- Enforce scope, rate limits, safety constraints, and Rules of Engagement from
  the task.
- Return observations, finding references, and evidence references only.

---

# Non-Responsibilities

The Active Testing Agent SHALL NOT:

- Execute any work without an approved [approval](../../schemas/approval.md).
- Execute tools directly; capability packages own execution.
- Produce Risk or presentation output.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying an Active Testing-tier capability,
target, scope reference, RoE reference, and an approved approval reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, `finding_refs`, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The Active Testing Agent coordinates the capability packages defined within
[skills/active-testing](../../skills/active-testing/README.md). Package selection
is an implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/active-testing](../../skills/active-testing/README.md) — the fronted
  tier.
- Canonical schemas: [task](../../schemas/task.md),
  [agent-response](../../schemas/agent-response.md),
  [approval](../../schemas/approval.md),
  [scope](../../schemas/scope.md),
  [rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- [Master Agent](../master/README.md)

---

# Success Criteria

- No task is coordinated without an approved approval reference.
- Every delegated Active Testing task is satisfied by coordinating tier packages.
- Results are returned by reference; no orchestration state is mutated.
