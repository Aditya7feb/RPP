# ADR-001 — Recon Orchestrator Skill

**File:** `skills/discovery/recon/adr/ADR-001-recon-orchestrator-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase comprises ten specialized skills, each performing one facet of
reconnaissance and each producing canonical
[Assets](../../../../schemas/asset.md),
[Findings](../../../../schemas/finding.md), and
[Evidence](../../../../schemas/evidence.md). An assessment needs a single entry
point that composes these skills into an ordered, policy-aware reconnaissance
workflow, separates passive work from active work, gates active work behind
approvals, and consolidates the outputs into one coherent result.

This orchestration is a distinct capability. It composes skills through the shared
[Workflow Runtime](../../../shared/workflow-runtime/README.md) using a
[Workflow Definition](../../../../schemas/workflow-definition.md) and delegates
graph consolidation to [Asset Discovery](../../asset-discovery/README.md). It must
perform no probing itself, keeping composition separate from execution.

---

# Decision

The platform SHALL provide a Recon Skill in the Discovery tier that

- Composes the Discovery skills into a
  [Workflow Definition](../../../../schemas/workflow-definition.md) with passive and
  active phases
- Requests phase authorization from the
  [Policy Engine](../../../shared/policy-engine/README.md) and inserts an approval
  gate before every active phase
- Drives execution through the
  [Workflow Runtime](../../../shared/workflow-runtime/README.md)
- Invokes [Asset Discovery](../../asset-discovery/README.md) to consolidate the
  produced asset graph
- Aggregates Findings, Observations, and Evidence from all composed skills into a
  single Discovery result

The skill SHALL perform no probing itself, SHALL NOT reimplement any composed
skill, SHALL NOT depend on any shared network client, and SHALL be tool
independent.

---

# Alternatives Considered

## A Monolithic Recon Skill

Recon could perform reconnaissance directly rather than composing skills.

Rejected because it would duplicate the specialized skills, couple unrelated
concerns, and violate the layered, single-responsibility design. Composition keeps
each skill focused and reusable.

## Orchestration Inside An Agent

The Recon Agent could sequence the skills directly without a Recon skill.

Rejected because reconnaissance sequencing, phase gating, and consolidation are
reusable platform capabilities that belong in a skill, not in agent logic. Agents
invoke the Recon skill instead.

## No Approval Gate Before Active Phases

Active phases could run automatically after passive phases.

Rejected because active reconnaissance is intrusive and Rules of Engagement often
require explicit authorization. An approval gate before active phases enforces
this deterministically.

---

# Consequences

## Positive

- Provides a single, policy-aware reconnaissance entry point
- Separates passive from active work with explicit approval gates
- Reuses specialized skills and the Workflow Runtime without duplication
- Delegates consolidation to Asset Discovery, keeping responsibilities clean
- Adds no network attack surface

## Negative

- Introduces dependencies on the Workflow Runtime and Policy Engine
- Requires careful phase and approval sequencing

The negative consequences are outweighed by cohesion, safety, and reuse.

---

# Compliance

The skill SHALL

- Perform no probing itself
- Authorize every phase and gate every active phase behind approval
- Compose skills only through the Workflow Runtime
- Invoke Asset Discovery for consolidation
- Preserve all aggregated Evidence
- Never weaken the policy constraints of composed skills

---

# Future Compatibility

Future versions MAY add adaptive profiles, iterative re-reconnaissance, and
policy-bounded parallel phase execution. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Recon README](../README.md)
- [Recon Interface](../interface.md)
- [Recon Execution Model](../execution.md)
- [Recon Error Model](../error-model.md)
- [Workflow Runtime](../../../shared/workflow-runtime/README.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Asset Discovery](../../asset-discovery/README.md)
- [Workflow Definition Schema](../../../../schemas/workflow-definition.md)
