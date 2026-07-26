# Authentication Agent

**File:** `agents/authentication/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Authentication Agent is the specialist tier agent that fronts the
Authentication capability tier. It accepts delegated authentication work from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/authentication](../../skills/authentication/README.md), and returns
structured results by reference.

The Authentication Agent is a thin coordinator. It contains no domain business
logic; all identity and session analysis logic lives in the Authentication
capability packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the
  Authentication tier.
- Select and order the Authentication capability packages required to satisfy it.
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, findings, and evidence.

---

# Owned Capability Tier

[skills/authentication](../../skills/authentication/README.md) — identity,
credential, session, and token analysis.

---

# Responsibilities

The Authentication Agent SHALL:

- Coordinate intra-tier ordering of Authentication packages.
- Enforce scope, authentication boundaries, and Rules of Engagement from the
  task.
- Return observations, finding references, and evidence references only.

---

# Non-Responsibilities

The Authentication Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Perform intrusive authentication-bypass validation without an approved
  [approval](../../schemas/approval.md); such validation is delegated by the
  Master Agent to the [Active Testing Agent](../active-testing/README.md).
- Produce Risk or presentation output.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying an Authentication-tier
capability, target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, `finding_refs`, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The Authentication Agent coordinates the capability packages defined within
[skills/authentication](../../skills/authentication/README.md). Package selection
is an implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/authentication](../../skills/authentication/README.md) — the fronted
  tier.
- Canonical schemas: [task](../../schemas/task.md),
  [agent-response](../../schemas/agent-response.md),
  [scope](../../schemas/scope.md),
  [rules-of-engagement](../../schemas/rules-of-engagement.md),
  [approval](../../schemas/approval.md).

---

# Related

- [Master Agent](../master/README.md)

---

# Success Criteria

- Every delegated Authentication task is satisfied by coordinating tier packages.
- Intrusive validation is gated and delegated, never performed here unbidden.
- Results are returned by reference; no orchestration state is mutated.
