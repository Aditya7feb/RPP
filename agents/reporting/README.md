# Reporting Agent

**File:** `agents/reporting/README.md`

**Version:** 1.0.0

**Agent Type:** Specialist Tier Agent

---

# Purpose

The Reporting Agent is the specialist tier agent that fronts the Reporting
capability tier. It accepts the delegated reporting pipeline from the
[Master Agent](../master/README.md), coordinates the capability packages within
[skills/reporting](../../skills/reporting/README.md) in order, and returns
structured results by reference.

The Reporting Agent is a thin coordinator. It contains no domain business logic;
all correlation, analysis, generation, and bundling logic lives in the Reporting
capability packages. Reporting is read-only over its inputs.

---

# Role

- Accept a [task](../../schemas/task.md) whose capability belongs to the Reporting
  tier.
- Coordinate the reporting pipeline in the canonical order:
  finding-correlation → risk-analysis → report-generation → evidence-bundle.
- Return an [agent-response](../../schemas/agent-response.md) referencing the
  correlated findings, analysis, generated reports, and evidence bundle.

---

# Owned Capability Tier

[skills/reporting](../../skills/reporting/README.md) — finding correlation, risk
analysis, finding mapping, report generation, and evidence bundling. All Reporting
capabilities are read-only over Findings, Risk, and Evidence.

---

# Responsibilities

The Reporting Agent SHALL:

- Coordinate the Reporting packages in pipeline order.
- Pass Findings, Risk, and Evidence to the packages **by reference only**.
- Return references to the correlated, analyzed, generated, and bundled outputs.

---

# Non-Responsibilities

The Reporting Agent SHALL NOT:

- Execute tools directly; capability packages own execution.
- Create, modify, deduplicate, or score Findings, Evidence, or canonical Risk
  itself; those are performed by the Reporting capability packages, and canonical
  Risk remains owned by the Domain Security tiers.
- Modify orchestration state.

---

# Delegation Contract

Input: a [task](../../schemas/task.md) carrying a Reporting-tier capability and
references to the Findings, Risk, and Evidence to present.

Output: an [agent-response](../../schemas/agent-response.md) carrying references
to the correlated findings, risk analysis, generated reports, and evidence
bundle.

---

# Coordinated Packages

The Reporting Agent coordinates the capability packages defined within
[skills/reporting](../../skills/reporting/README.md): finding-correlation,
risk-analysis, finding-mapping, report-generation, and evidence-bundle. Package
selection is an implementation detail of the tier and is opaque to the Master
Agent.

---

# Dependencies

- [skills/reporting](../../skills/reporting/README.md) — the fronted tier.
- Canonical schemas: [task](../../schemas/task.md),
  [agent-response](../../schemas/agent-response.md),
  [report](../../schemas/report.md).

---

# Related

- [Master Agent](../master/README.md)

---

# Success Criteria

- The reporting pipeline is coordinated in canonical order.
- Findings, Risk, and Evidence are consumed by reference and remain immutable.
- No correlation, scoring, or rendering logic executes in the agent layer.
