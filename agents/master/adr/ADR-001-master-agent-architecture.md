# ADR-001: Master Agent Architecture

**File:** `agents/master/adr/ADR-001-master-agent-architecture.md`

**Version:** 1.0.0

**Status:** Accepted

---

# Context

The `agents/` layer was authored before the repository standardized on a
capability-oriented, schema-first, tool-independent architecture across the
capability tiers. As a result the original Master Agent specification:

- Referenced tools directly (violating tool independence).
- Organized delegation around a legacy taxonomy (recon, scanners, exploit,
  execution, knowledge) that did not map to the canonical capability tiers.
- Absorbed business logic owned by other tiers — finding deduplication,
  correlation, prioritization, attack-chain construction, evidence collection,
  and confidence definition.
- Contained no references to the canonical schemas it was meant to coordinate.

This produced ownership overlap with the Reporting, Evidence, and Domain Security
tiers, a duplicated confidence model, and an orchestration layer disconnected
from the canonical schemas.

---

# Decision

The Master Agent is defined as a **pure orchestrator**, normalized into the
canonical package structure, and integrated with the existing architecture.

1. **Pure orchestration.** The Master Agent owns planning, reasoning,
   delegation, workflow coordination, approval gating, execution tracking, and
   completion. It owns no Findings, Evidence, Risk, or Reporting logic.

2. **Capability-oriented taxonomy.** The legacy taxonomy is replaced by the eight
   canonical capability tiers: Discovery, Authentication, Web Security, API
   Security, Cloud, Active Testing, Evidence, and Reporting. All delegation
   targets capabilities, never tools.

3. **One specialist agent per capability tier.** Each tier is fronted by a single
   specialist tier agent that coordinates the packages within its tier. Packages
   remain implementation details inside each capability tier.

4. **Schema binding, no new schemas.** Orchestration binds to the existing
   canonical schemas: assessment, scope, rules-of-engagement, execution-plan,
   execution-state, task, agent-response, approval, and workflow-definition.

5. **Reference-based reporting integration.** The Master Agent invokes
   finding-correlation, risk-analysis, report-generation, and evidence-bundle in
   order and consumes their outputs by reference only.

6. **Single confidence source.** Confidence semantics are referenced from
   `skills/core/confidence-model`; the Master Agent does not redefine them.

7. **Orchestration-only memory.** Memory supports orchestration exclusively.
   Capabilities remain deterministic and never depend on orchestration memory.

---

# Consequences

## Positive

- Restores the ownership boundaries established across the capability tiers.
- Removes tool coupling from the top of the architecture.
- Reduces the delegation surface from many packages to eight tier agents.
- Eliminates the duplicated confidence model.
- Guarantees deterministic, memory-independent capabilities.

## Negative

- Requires migrating the legacy taxonomy and consolidating the prior ad-hoc
  policy documents into the canonical package files.

## Neutral

- The migration is staged: the taxonomy and references are updated first, and the
  obsolete stub folders are removed only once no references remain.

---

# Alternatives Considered

- **One specialist agent per capability package.** Rejected: it produces a large
  delegation surface, forces the Master Agent to micro-schedule intra-tier work,
  and risks the orchestrator absorbing capability sequencing logic.
- **Retaining the legacy taxonomy.** Rejected: it does not map to the canonical
  tiers, omits Cloud, API, and Active Testing, and is organized by tool phase
  rather than capability.
- **Introducing new orchestration schemas.** Rejected: the existing canonical
  schemas fully cover orchestration intake, planning, delegation, state, gating,
  and workflow coordination.

---

# Related

- [Master Agent README](../README.md)
- [Master Agent Interface](../interface.md)
- [Master Agent Execution Model](../execution.md)
- [skills/core/confidence-model.md](../../../skills/core/confidence-model.md)
- [skills/reporting/README.md](../../../skills/reporting/README.md)
