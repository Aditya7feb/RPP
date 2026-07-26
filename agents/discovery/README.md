# Discovery Agent

**File:** `agents/discovery/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Discovery Agent is the specialist tier agent that fronts the Discovery
capability tier. It accepts delegated discovery work from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/discovery](../../skills/discovery/README.md), and returns structured
results by reference.

The Discovery Agent is a thin coordinator. It contains no domain business logic;
all attack-surface enumeration logic lives in the Discovery capability packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the
  Discovery tier.
- Select and order the Discovery capability packages required to satisfy it.
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, assets, and evidence.

---

# Owned Capability Tier

[skills/discovery](../../skills/discovery/README.md) — attack-surface discovery,
including subdomain, host, port, service, endpoint, and technology enumeration.

---

# Responsibilities

The Discovery Agent SHALL:

- Coordinate intra-tier ordering of Discovery packages.
- Enforce scope and Rules of Engagement received in the task.
- Return observations, asset references, and evidence references only.

---

# Non-Responsibilities

The Discovery Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Produce Risk or presentation output.
- Perform work owned by other tiers (authentication, web, api, cloud, active
  testing, evidence, reporting).
- Modify orchestration state; only the Master Agent does.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying a Discovery-tier capability,
target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, asset references, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The Discovery Agent coordinates the capability packages defined within
[skills/discovery](../../skills/discovery/README.md). Package selection is an
implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/discovery](../../skills/discovery/README.md) — the fronted tier.
- Canonical schemas: [task](../../schemas/task.md),
  [agent-response](../../schemas/agent-response.md),
  [scope](../../schemas/scope.md),
  [rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- [Master Agent](../master/README.md)

---

# Success Criteria

- Every delegated Discovery task is satisfied by coordinating tier packages.
- Results are returned by reference; no orchestration state is mutated.
- No capability logic executes in the agent layer.
