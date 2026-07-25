# Asset Discovery Interface

**File:** `skills/discovery/asset-discovery/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the
Asset Discovery Skill. Consumers depend only on this contract.

---

# Interface Overview

```
consolidate_assets(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: consolidate_assets

## Request

```yaml
assets:

relationships:

evidence:

scope_id:

roe_id:

assessment_id:
```

- `assets` (required) — canonical [Assets](../../../schemas/asset.md) produced by
  other Discovery skills.
- `relationships` (optional) — canonical
  [Asset Relationships](../../../schemas/asset-relationship.md).
- `evidence` (optional) — [Evidence](../../../schemas/evidence.md) references
  supporting the inputs.
- `scope_id` (required) — the assessment [Scope](../../../schemas/scope.md).
- `roe_id` (required) — the
  [Rules of Engagement](../../../schemas/rules-of-engagement.md).
- `assessment_id` (optional) — correlating assessment identifier.

---

## Result

```yaml
assets:

relationships:

observations:

evidence:

findings:

status:

metrics:
```

- `assets` — the consolidated, deduplicated, scope-confirmed Assets.
- `relationships` — reconciled Asset Relationships.
- `observations` — [Observations](../../../schemas/observation.md) for
  consolidation decisions.
- `evidence` — [Evidence](../../../schemas/evidence.md) references.
- `findings` — [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for structural problems.
- `status` — one of `completed`, `partial`, `error`.
- `metrics` — counters such as Assets ingested and duplicates merged.

---

# Behavioral Contract

The skill SHALL

- Perform no network activity
- Confirm `scope_status` through the
  [Policy Engine](../../shared/policy-engine/README.md)
- Deduplicate and merge Assets conservatively, preserving provenance
- Reconcile Relationships into a coherent graph
- Record Observations and promote Evidence for every decision
- Emit Findings only with supporting Evidence
- Never invent Assets absent from the inputs

The skill SHALL NOT

- Probe, scan, resolve, or request any target
- Depend on a shared network client
- Produce Findings requiring active verification

---

# Error Semantics

Errors are reported per the [error model](error-model.md). Malformed inputs yield
`error`. Partial consolidation yields `partial` with Evidence for completed
decisions.

---

# Interface Stability

This interface is stable within the `1.x` series. Backward-compatible additions
MAY introduce new optional request fields and result counters. Breaking changes
SHALL increment the major version.

---

# Related Documents

- [Capabilities](capabilities.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Policy Engine Interface](../../shared/policy-engine/interface.md)
