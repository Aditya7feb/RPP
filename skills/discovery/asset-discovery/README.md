# Asset Discovery Skill

**File:** `skills/discovery/asset-discovery/README.md`

**Version:** 1.0.0

---

# Purpose

The Asset Discovery Skill is a Discovery-tier domain skill that consolidates the
asset graph produced by the other Discovery skills within the Robust PenTest
Platform (RPP).

It is an *aggregator*. It does not probe targets. It ingests the canonical
[Assets](../../../schemas/asset.md) and
[Asset Relationships](../../../schemas/asset-relationship.md) emitted by skills such
as DNS Enumeration, Port Discovery, Subdomain Discovery, Content Discovery,
Fingerprinting, API Discovery, and Endpoint Enumeration, then deduplicates,
merges, and links them into a single coherent asset graph.

Where the consolidated graph reveals structural problems — orphan assets,
conflicting facts, or out-of-scope inclusions — the skill emits
[Observations](../../../schemas/observation.md) and, where warranted,
[Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md). It
performs no network activity and invokes no tools.

---

# Goals

The Asset Discovery Skill SHALL

- Ingest Assets and Asset Relationships produced by other Discovery skills
- Deduplicate and merge Assets that denote the same real-world entity
- Build and reconcile Asset Relationships into a coherent graph
- Confirm the `scope_status` of every Asset against the assessment Scope
- Emit Observations and Evidence for every consolidation decision
- Flag orphan, conflicting, or out-of-scope Assets as Findings where warranted
- Consult the [Policy Engine](../../shared/policy-engine/README.md) for scope
  confirmation
- Remain tool independent and perform no network activity

---

# Non-Goals

The Asset Discovery Skill SHALL NOT

- Probe, scan, resolve, or request any target
- Depend on any shared network client
- Discover new Assets through active means
- Produce Findings that require active verification
- Test Assets for vulnerabilities
- Invoke command-line tools or parse their output

All active discovery belongs to the other Discovery skills. This skill only
consolidates their outputs.

---

# Design Principles

The Asset Discovery Skill SHALL be

- Passive and non-intrusive — it consumes existing outputs only
- Deterministic given the same input asset graph
- Evidence-backed for every merge, link, and flag
- Conservative in merging — it SHALL NOT merge Assets without sufficient evidence
- Scope-aware — every consolidated Asset carries a confirmed `scope_status`
- Tool independent

---

# Architecture

```
Recon Agent / Discovery Skills

↓  (Assets · Relationships · Evidence)

Asset Discovery Skill

├── Scope Confirmer        → Policy Engine
├── Deduplicator
├── Merger
├── Relationship Reconciler
├── Consistency Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Consolidated Asset Graph · Observations · Evidence · Findings · Risk
```

The skill consumes canonical objects and produces a consolidated graph. It has no
transport dependency of any kind.

---

# Responsibilities

The Asset Discovery Skill is responsible for

- Ingesting Assets, Relationships, Observations, and Evidence from other skills
- Deduplicating Assets by canonical identity
- Merging duplicate Assets while preserving provenance from every source
- Reconciling and completing Asset Relationships
- Confirming `scope_status` through the
  [Policy Engine](../../shared/policy-engine/README.md)
- Detecting orphan, conflicting, and out-of-scope Assets
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md) for every decision
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) where structural problems warrant

---

# Discovery Lifecycle

```
Receive Asset Graph From Discovery Skills

↓

Confirm Scope (Policy Engine)

↓

Deduplicate Assets By Canonical Identity

↓

Merge Duplicates (preserve provenance)

↓

Reconcile Relationships

↓

Analyze Consistency

↓

Record Observations → Evidence

↓

Emit Findings And Risk (where warranted)

↓

Return Consolidated Graph
```

Every consolidation decision SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
assets:

relationships:

evidence:

scope_id:

roe_id:
```

`assets` and `relationships` SHALL be canonical objects produced by other
Discovery skills. `evidence` references support their provenance. `scope_id` and
`roe_id` reference the assessment [Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce a consolidated set of canonical
[Assets](../../../schemas/asset.md) in which duplicates are merged and each Asset
carries

- Aggregated provenance from every contributing source
- A confirmed `scope_status`
- Reconciled [Asset Relationships](../../../schemas/asset-relationship.md)

The skill SHALL NOT invent Assets that were not present in its inputs.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for structural problems such as

- Out-of-scope Assets that were reported by an active skill
- Conflicting facts about the same Asset across sources
- Orphan Assets with no supporting relationship or provenance

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).
The skill SHALL NOT emit Findings that would require active verification.

---

# Policy Enforcement

The Asset Discovery Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) to confirm the
`scope_status` of consolidated Assets. Because the skill performs no network
activity, no `active` action decision is required; scope confirmation is the sole
policy interaction. Assets confirmed out of scope SHALL be flagged and excluded
from the in-scope graph.

---

# Dependencies

The Asset Discovery Skill depends on

- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)
- [Scope Schema](../../../schemas/scope.md)

The Asset Discovery Skill SHALL NOT depend on any shared network client or on any
other domain skill.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows, which present the consolidated graph
- Downstream tiers that operate on a deduplicated, scope-confirmed asset graph
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- A consolidated, deduplicated Asset graph with reconciled relationships
- Observations and Evidence for every consolidation decision
- Findings with Risk for structural problems

Outputs SHALL remain implementation independent.

---

# Security Principles

The Asset Discovery Skill SHALL

- Perform no network activity of any kind
- Confirm scope through the Policy Engine and exclude out-of-scope Assets
- Merge conservatively, never on insufficient evidence
- Preserve provenance from every contributing source
- Produce no Finding without supporting Evidence
- Preserve auditability of every merge and flag

---

# Best Practices

Consumers SHOULD

- Provide the complete asset graph from all Discovery skills
- Run this skill after active Discovery skills complete
- Treat the consolidated graph as the canonical Discovery output
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect this skill to discover new Assets actively
- Provide it a network client or ask it to probe
- Bypass scope confirmation
- Merge Assets manually without provenance

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-asset-discovery-skill.md

---

# Related Packages

- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [DNS Enumeration](../dns-enumeration/README.md)
- [Port Discovery](../port-discovery/README.md)
- [Subdomain Discovery](../subdomain-discovery/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)
- [Scope](../../../schemas/scope.md)

---

# Architecture Decisions

- [ADR-001 — Asset Discovery Skill](adr/ADR-001-asset-discovery-skill.md)

---

# Future Extensions

Future versions MAY support

- Cross-assessment asset correlation
- Probabilistic entity resolution with confidence scoring
- Asset graph diffing across time
- Persistent asset-graph storage, subject to a future Architecture Proposal

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Asset Discovery Skill consolidates the Discovery asset graph into a
single deduplicated, scope-confirmed, evidence-backed set of canonical Assets and
Relationships, flags structural problems as Findings, and performs no network
activity, invoking no tools directly.
