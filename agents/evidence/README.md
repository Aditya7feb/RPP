# Evidence Agent

**File:** `agents/evidence/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Evidence Agent is the specialist tier agent that fronts the Evidence
capability tier. It accepts delegated evidence capture and correlation work from
the [Master Agent](../master/README.md), coordinates the capability packages
within [skills/evidence](../../skills/evidence/README.md), and returns structured
results by reference.

The Evidence Agent is a thin coordinator. It contains no domain business logic;
all capture, correlation, and promotion logic lives in the Evidence capability
packages and the shared evidence infrastructure they invoke.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the Evidence
  tier.
- Select and order the Evidence capability packages required to satisfy it
  (screenshot capture, HTTP archive, network trace, artifact collection, log
  collection, timeline).
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  captured and correlated evidence.

---

# Owned Capability Tier

[skills/evidence](../../skills/evidence/README.md) — evidence capture, artifact
collection, and correlation; promotion of transient artifacts to durable Evidence
through the shared evidence infrastructure.

---

# Responsibilities

The Evidence Agent SHALL:

- Coordinate intra-tier ordering of Evidence packages.
- Enforce scope and Rules of Engagement on target-facing captures received in the
  task.
- Return evidence references only; Evidence is immutable once produced.

---

# Non-Responsibilities

The Evidence Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Produce Findings, Risk, or presentation output.
- Infer, classify, or prioritize security meaning; the timeline package
  correlates but does not analyze.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying an Evidence-tier capability,
target, scope reference, and RoE reference.

Output: an [agent-response](../../schemas/agent-response.md) carrying
`evidence_refs` and `observation_refs`, plus optional `next_recommended`
capabilities.

---

# Coordinated Packages

The Evidence Agent coordinates the capability packages defined within
[skills/evidence](../../skills/evidence/README.md). Package selection is an
implementation detail of the tier and is opaque to the Master Agent.

---

# Dependencies

- [skills/evidence](../../skills/evidence/README.md) — the fronted tier.
- Canonical schemas: [task](../../schemas/task.md),
  [agent-response](../../schemas/agent-response.md),
  [scope](../../schemas/scope.md),
  [rules-of-engagement](../../schemas/rules-of-engagement.md).

---

# Related

- [Master Agent](../master/README.md)

---

# Success Criteria

- Every delegated Evidence task is satisfied by coordinating tier packages.
- Evidence is returned by reference and remains immutable.
- No Finding, Risk, or presentation logic executes in the agent layer.
