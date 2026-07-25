# Asset Discovery Capabilities

**File:** `skills/discovery/asset-discovery/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Asset Discovery Skill.
Capabilities describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Asset Discovery Interface](interface.md).

---

# Capability Model

```
Scope Confirmation

Deduplication

Merging

Relationship Reconciliation

Consistency Analysis

Observability
```

---

# Scope Confirmation Capabilities

## Scope Confirmation

The skill SHALL confirm the `scope_status` of every Asset through the
[Policy Engine](../../shared/policy-engine/README.md).

---

## Out-Of-Scope Exclusion

The skill SHALL exclude out-of-scope Assets from the in-scope graph.

---

# Deduplication Capabilities

## Canonical Identity Matching

The skill SHALL identify duplicate [Assets](../../../schemas/asset.md) by canonical
identity.

---

## Conservative Deduplication

The skill SHALL NOT treat Assets as duplicates without sufficient evidence.

---

# Merging Capabilities

## Asset Merging

The skill SHALL merge duplicate Assets into a single canonical Asset.

---

## Provenance Preservation

The skill SHALL preserve provenance from every contributing source on the merged
Asset.

---

# Relationship Reconciliation Capabilities

## Relationship Reconciliation

The skill SHALL reconcile and complete
[Asset Relationships](../../../schemas/asset-relationship.md) across merged Assets.

---

## Graph Coherence

The skill SHALL produce a coherent asset graph free of dangling relationship
endpoints.

---

# Consistency Analysis Capabilities

## Conflict Detection

The skill SHALL detect conflicting facts about the same Asset across sources.

---

## Orphan Detection

The skill SHALL detect orphan Assets lacking provenance or relationships.

---

## Finding Production

The skill SHALL produce [Findings](../../../schemas/finding.md) with
[Risk](../../../schemas/risk.md) for structural problems, each backed by Evidence.

---

# Observability Capabilities

## Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) and promote
them to [Evidence](../../../schemas/evidence.md) for every consolidation decision.

---

## Event Emission

The skill SHOULD publish lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including Assets ingested, duplicates merged, and
conflicts detected.

---

# Capability Boundaries

The skill SHALL NOT

- Perform network activity of any kind
- Discover new Assets actively
- Test Assets for vulnerabilities
- Produce a Finding without Evidence
- Merge Assets on insufficient evidence

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Scope Confirmation | Scope Confirmation | SHALL |
| Out-Of-Scope Exclusion | Scope Confirmation | SHALL |
| Canonical Identity Matching | Deduplication | SHALL |
| Conservative Deduplication | Deduplication | SHALL |
| Asset Merging | Merging | SHALL |
| Provenance Preservation | Merging | SHALL |
| Relationship Reconciliation | Relationship Reconciliation | SHALL |
| Graph Coherence | Relationship Reconciliation | SHALL |
| Conflict Detection | Consistency Analysis | SHALL |
| Orphan Detection | Consistency Analysis | SHALL |
| Finding Production | Consistency Analysis | SHALL |
| Observation And Evidence | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
