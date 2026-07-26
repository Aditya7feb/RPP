# Parameter Mining Interface

**File:** `skills/active-testing/parameter-mining/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Parameter Mining
Capability.

---

# Operation: mine

## Request

```yaml
mine:
  target:
  locations:
  candidate_source:
    wordlist_name:
    max_candidates:
  bounds:
    max_requests:
  scope_id:
  roe_id:
```

`target` SHALL be an in-scope endpoint. `locations` selects probe locations.
`candidate_source` draws candidate names. `bounds` limits request volume.

## Response

```yaml
mine_result:
  target:
  observations:
  artifact_refs:
  metrics_ref:
  decision_summary:
```

`observations` reference [Observations](../../../schemas/observation.md); `artifact_refs`
reference [Artifacts](../../../schemas/artifact.md); `metrics_ref` references
[Metrics](../../../schemas/metrics.md). No Findings or Risk are produced.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- `max_requests` SHALL be a positive integer when present.

---

# Postconditions

- Every probe SHALL have been policy-gated.
- Probing SHALL have remained non-destructive and bounded.
- No out-of-scope target SHALL have been contacted.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `mine` operation is stable. Additional locations and detection modes MAY be introduced in
a backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
