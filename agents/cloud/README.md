# Cloud Agent

**File:** `agents/cloud/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Cloud Agent is the specialist tier agent that fronts the Cloud Security
capability tier. It accepts delegated cloud posture work from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/cloud](../../skills/cloud/README.md), and returns structured results by
reference.

The Cloud Agent is a thin coordinator. It contains no domain business logic; all
cloud posture analysis lives in the Cloud capability packages.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the Cloud
  Security tier.
- Select and order the Cloud capability packages required to satisfy it (AWS,
  Azure, GCP, Kubernetes, Docker, and Terraform posture).
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  produced observations, findings, and evidence.

---

# Owned Capability Tier

[skills/cloud](../../skills/cloud/README.md) — cloud and container posture
analysis across AWS, Azure, GCP, Kubernetes, Docker, and Terraform.

---

# Responsibilities

The Cloud Agent SHALL:

- Coordinate intra-tier ordering of Cloud packages by provider and surface.
- Enforce scope, authentication boundaries, and Rules of Engagement from the
  task.
- Return observations, finding references, and evidence references only.

---

# Non-Responsibilities

The Cloud Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Perform state-changing validation without an approved
  [approval](../../schemas/approval.md); such validation is delegated by the
  Master Agent to the [Active Testing Agent](../active-testing/README.md).
- Produce Risk or presentation output.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying a Cloud Security-tier capability,
target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`observation_refs`, `finding_refs`, and `evidence_refs`, plus optional
`next_recommended` capabilities.

---

# Coordinated Packages

The Cloud Agent coordinates the capability packages defined within
[skills/cloud](../../skills/cloud/README.md). Package selection is an
implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/cloud](../../skills/cloud/README.md) — the fronted tier.
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

- Every delegated Cloud task is satisfied by coordinating tier packages.
- State-changing validation is gated and delegated, never performed here unbidden.
- Results are returned by reference; no orchestration state is mutated.
