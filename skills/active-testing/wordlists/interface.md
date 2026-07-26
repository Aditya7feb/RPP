# Wordlists Interface

**File:** `skills/active-testing/wordlists/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Wordlists
Capability.

---

# Operation: select

## Request

```yaml
select:
  list_name:
  selection:
    filter:
    max_entries:
  emit:
    as_artifact:
    as_seeds:
```

`list_name` SHALL name a registered list. `selection` bounds the result. `emit` selects the
output form.

## Response

```yaml
select_result:
  list_name:
  list_version:
  entry_count:
  artifact_ref:
  seed_refs:
  metrics_ref:
```

`artifact_ref` references an [Artifact](../../../schemas/artifact.md); `seed_refs`
reference [Payload](../../../schemas/payload.md) seeds; `metrics_ref` references
[Metrics](../../../schemas/metrics.md).

---

# Preconditions

- `list_name` SHALL resolve to a registered list.
- `max_entries` SHALL be a positive integer when present.

---

# Postconditions

- Output SHALL be bounded by `max_entries`.
- No target SHALL have been contacted.
- No Findings or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md). The interface SHALL surface
deterministic outcomes.

---

# Interface Stability

The `select` operation is stable. Additional selection criteria MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
