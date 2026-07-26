# Web Security Agent

**File:** `agents/web-security/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Web Security Agent is the specialist tier agent that fronts the Web Security
capability tier. It accepts delegated web-application security work from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/web-security](../../skills/web-security/README.md), and returns structured
results by reference.

The Web Security Agent is a thin coordinator. It contains no domain business
logic; all web-application security analysis lives in the Web Security capability
packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the Web
  Security tier.
- Select and order the Web Security capability packages required to satisfy it.
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, findings, and evidence.

---

# Owned Capability Tier

[skills/web-security](../../skills/web-security/README.md) — web-application
security analysis, including headers, content, injection surfaces, and
client-side posture.

---

# Responsibilities

The Web Security Agent SHALL:

- Coordinate intra-tier ordering of Web Security packages.
- Enforce scope, excluded paths, rate limits, and Rules of Engagement from the
  task.
- Return observations, finding references, and evidence references only.

---

# Non-Responsibilities

The Web Security Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Perform payload-driven validation that changes target state without an approved
  [approval](../../schemas/approval.md); such validation is delegated by the
  Master Agent to the [Active Testing Agent](../active-testing/README.md).
- Produce Risk or presentation output.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying a Web Security-tier capability,
target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, `finding_refs`, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The Web Security Agent coordinates the capability packages defined within
[skills/web-security](../../skills/web-security/README.md). Package selection is
an implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/web-security](../../skills/web-security/README.md) — the fronted tier.
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

- Every delegated Web Security task is satisfied by coordinating tier packages.
- State-changing validation is gated and delegated, never performed here unbidden.
- Results are returned by reference; no orchestration state is mutated.
