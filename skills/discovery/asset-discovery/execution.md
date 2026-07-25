# Asset Discovery Execution Model

**File:** `skills/discovery/asset-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Asset Discovery
Skill, stage by stage. Given the same input asset graph and configuration,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Confirm Scope (Policy Engine)

↓

Deduplicate Assets

↓

Merge Duplicates

↓

Reconcile Relationships

↓

Analyze Consistency

↓

Record Observations → Evidence

↓

Emit Findings And Risk

↓

Return Consolidated Graph
```

The skill performs no network activity at any stage.

---

# Stage 1 — Validate Request

The skill SHALL validate that `assets`, `scope_id`, and `roe_id` are present and
that Assets are canonical. Invalid requests SHALL fail closed with a validation
error.

---

# Stage 2 — Confirm Scope

The skill SHALL confirm the `scope_status` of every Asset through the
[Policy Engine](../../shared/policy-engine/README.md). Because no target-facing
action occurs, only scope confirmation is required. Assets confirmed out of scope
SHALL be excluded from the in-scope graph and flagged where reported by an active
skill.

---

# Stage 3 — Deduplicate Assets

The skill SHALL identify duplicate [Assets](../../../schemas/asset.md) by canonical
identity using the configured strategy and confidence threshold. Assets below the
threshold SHALL NOT be treated as duplicates.

---

# Stage 4 — Merge Duplicates

The skill SHALL merge confirmed duplicates into a single canonical Asset,
preserving provenance from every contributing source. Conflicting facts SHALL be
handled per the configured conflict policy and never silently discarded.

---

# Stage 5 — Reconcile Relationships

The skill SHALL update
[Asset Relationships](../../../schemas/asset-relationship.md) to reference merged
Asset identities and SHALL remove or flag dangling relationships per
configuration, producing a coherent graph.

---

# Stage 6 — Analyze Consistency

The skill SHALL analyze the consolidated graph for orphan Assets, conflicting
facts, and out-of-scope inclusions using deterministic criteria. Analysis is
separate from merging.

---

# Stage 7 — Record Observations And Evidence

Every consolidation decision — merge, link, exclusion, or flag — SHALL yield an
[Observation](../../../schemas/observation.md) promoted to
[Evidence](../../../schemas/evidence.md).

---

# Stage 8 — Emit Findings And Risk

Where a structural problem warrants, the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding requiring active verification SHALL be
emitted.

---

# Stage 9 — Return Consolidated Graph

The skill SHALL return the consolidated Assets, reconciled relationships,
observations, evidence, findings, a `status`, and metrics per the
[interface](interface.md).

---

# Determinism Guarantees

- Same input graph and configuration yield the same consolidated graph.
- Merging is conservative and evidence-bound.
- Analysis is separated from merging.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial consolidation
SHALL return completed decisions with Evidence. Validation errors SHALL fail
closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
