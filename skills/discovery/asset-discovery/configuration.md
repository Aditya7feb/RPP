# Asset Discovery Configuration

**File:** `skills/discovery/asset-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Asset Discovery Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
asset_discovery:

  deduplication:
    match_strategy:
    min_match_confidence:

  merging:
    preserve_all_provenance:
    conflict_policy:

  relationships:
    reconcile:
    drop_dangling:

  consistency:
    flag_orphans:
    flag_conflicts:
    flag_out_of_scope:

  evidence:
    record_decisions:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Deduplication

- `match_strategy` — the canonical identity strategy used to match duplicates
  (for example, by normalized value and type). Default `canonical-identity`.
- `min_match_confidence` — the minimum confidence required to treat two Assets as
  duplicates. Assets below this threshold SHALL NOT be merged.

---

## Merging

- `preserve_all_provenance` — whether provenance from every source is retained on
  the merged Asset. Default `true` and SHALL NOT be disabled.
- `conflict_policy` — how conflicting facts are handled: `retain-both`,
  `prefer-higher-confidence`, or `flag-only`. Default `flag-only`; conflicts are
  never silently discarded.

---

## Relationships

- `reconcile` — whether relationships are reconciled across merged Assets. Default
  `true`.
- `drop_dangling` — whether relationships with a missing endpoint are dropped or
  flagged. Default `false`; dangling relationships are flagged, not silently
  dropped, unless explicitly enabled.

---

## Consistency

- `flag_orphans` — whether orphan Assets are flagged. Default `true`.
- `flag_conflicts` — whether conflicting facts are flagged. Default `true`.
- `flag_out_of_scope` — whether out-of-scope Assets reported by active skills are
  flagged. Default `true`.

---

## Evidence

- `record_decisions` — whether every consolidation decision records Evidence.
  Default `true` and SHALL NOT be disabled.

---

## Policy

- `scope_id` — the [Scope](../../../schemas/scope.md) reference.
- `roe_id` — the [Rules of Engagement](../../../schemas/rules-of-engagement.md)
  reference.

---

# Precedence

Configuration resolves in the following order, later overriding earlier, except
that scope confirmation SHALL NOT be weakened:

```
Skill Defaults

↓

Assessment Configuration

↓

Request Parameters

↓

Policy Engine Scope Decision (authoritative for scope_status)
```

The [Policy Engine](../../shared/policy-engine/README.md) scope decision SHALL
always determine `scope_status`.

---

# Validation Rules

- `scope_id` and `roe_id` SHALL be present.
- `min_match_confidence` SHALL be within its defined range.
- `preserve_all_provenance` SHALL NOT be disabled.
- `record_decisions` SHALL NOT be disabled.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Asset Schema](../../../schemas/asset.md)
