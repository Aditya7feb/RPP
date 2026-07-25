# ADR-001 — Asset Discovery Skill

**File:** `skills/discovery/asset-discovery/adr/ADR-001-asset-discovery-skill.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Discovery phase comprises multiple skills, each producing canonical
[Assets](../../../../schemas/asset.md) and
[Asset Relationships](../../../../schemas/asset-relationship.md) from its own
vantage point. The same real-world entity — a host, service, or endpoint — is
frequently reported by several skills, sometimes with conflicting facts. Without
consolidation, downstream tiers would operate on a fragmented, duplicated graph.

A dedicated aggregator is required to deduplicate, merge, and reconcile the asset
graph into a single coherent, scope-confirmed output. This aggregator must not
perform any active discovery; all probing belongs to the other Discovery skills.

This aligns with the Discovery-skill pattern for evidence and policy while
deliberately omitting any network dependency, distinguishing this skill from every
other Discovery skill.

---

# Decision

The platform SHALL provide an Asset Discovery Skill in the Discovery tier that

- Ingests Assets, Relationships, and Evidence produced by other Discovery skills
- Deduplicates and merges Assets by canonical identity, conservatively and with
  preserved provenance
- Reconciles [Asset Relationships](../../../../schemas/asset-relationship.md) into
  a coherent graph
- Confirms `scope_status` through the
  [Policy Engine](../../../shared/policy-engine/README.md)
- Detects orphan, conflicting, and out-of-scope Assets and emits
  [Findings](../../../../schemas/finding.md) with
  [Risk](../../../../schemas/risk.md) where warranted, backed by
  [Evidence](../../../../schemas/evidence.md)
- Records [Observations](../../../../schemas/observation.md) for every decision

The skill SHALL perform no network activity, SHALL NOT depend on any shared
network client, SHALL NOT discover Assets actively, and SHALL be tool independent.

---

# Alternatives Considered

## Consolidating Within Each Discovery Skill

Each skill could deduplicate against a shared graph as it runs.

Rejected because it couples skills to one another and to shared mutable state,
introduces ordering dependencies, and scatters consolidation logic. A dedicated
aggregator keeps each skill focused and consolidation centralized.

## Consolidating In The Recon Orchestrator

The Recon orchestrator could consolidate as part of composition.

Rejected because consolidation is a distinct, reusable capability with its own
evidence and findings. Embedding it in the orchestrator would conflate
composition with graph reconciliation. The orchestrator SHOULD invoke this skill
instead.

## Allowing Active Verification

The skill could actively verify conflicts or orphans.

Rejected because active verification belongs to the probing Discovery skills.
This skill consolidates existing outputs only and defers any active check to
those skills.

---

# Consequences

## Positive

- Produces a single deduplicated, scope-confirmed asset graph
- Centralizes consolidation with full provenance and evidence
- Keeps active Discovery skills decoupled and focused
- Adds no network attack surface; depends only on Policy Engine and Evidence

## Negative

- Introduces an additional Discovery step after active skills complete
- Requires conservative, evidence-bound merging to avoid false consolidation

The negative consequences are outweighed by graph coherence and safety.

---

# Compliance

The skill SHALL

- Perform no network activity
- Confirm scope through the Policy Engine and exclude out-of-scope Assets
- Merge conservatively with preserved provenance
- Never silently discard conflicting facts
- Back every Finding with Evidence
- Never invent Assets absent from its inputs

---

# Future Compatibility

Future versions MAY add cross-assessment correlation, probabilistic entity
resolution, and asset-graph diffing. Persistent asset-graph storage remains
subject to a separate Architecture Proposal. These extensions SHALL preserve the
existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Asset Discovery README](../README.md)
- [Asset Discovery Interface](../interface.md)
- [Asset Discovery Execution Model](../execution.md)
- [Asset Discovery Error Model](../error-model.md)
- [Policy Engine](../../../shared/policy-engine/README.md)
- [Evidence](../../../shared/evidence/README.md)
- [Asset Schema](../../../../schemas/asset.md)
- [Asset Relationship Schema](../../../../schemas/asset-relationship.md)
