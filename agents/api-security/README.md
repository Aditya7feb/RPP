# API Security Agent

**File:** `agents/api-security/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The API Security Agent is the specialist tier agent that fronts the API Security
capability tier. It accepts delegated API security work from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/api-security](../../skills/api-security/README.md), and returns structured
results by reference.

The API Security Agent is a thin coordinator. It contains no domain business
logic; all API security analysis lives in the API Security capability packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the API
  Security tier.
- Select and order the API Security capability packages required to satisfy it
  (REST, GraphQL, SOAP, gRPC, and WebSocket surfaces).
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, findings, and evidence.

---

# Owned Capability Tier

[skills/api-security](../../skills/api-security/README.md) — API security analysis
across REST, GraphQL, SOAP, gRPC, and WebSocket protocols.

---

# Responsibilities

The API Security Agent SHALL:

- Coordinate intra-tier ordering of API Security packages by protocol.
- Enforce scope, authentication boundaries, rate limits, and Rules of Engagement
  from the task.
- Return observations, finding references, and evidence references only.

---

# Non-Responsibilities

The API Security Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Perform state-changing validation without an approved
  [approval](../../schemas/approval.md); such validation is delegated by the
  Master Agent to the [Active Testing Agent](../active-testing/README.md).
- Produce Risk or presentation output.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying an API Security-tier capability,
target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, `finding_refs`, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The API Security Agent coordinates the capability packages defined within
[skills/api-security](../../skills/api-security/README.md). Package selection is
an implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/api-security](../../skills/api-security/README.md) — the fronted tier.
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

- Every delegated API Security task is satisfied by coordinating tier packages.
- State-changing validation is gated and delegated, never performed here unbidden.
- Results are returned by reference; no orchestration state is mutated.
