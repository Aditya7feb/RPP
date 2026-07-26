# Replay Interface

**File:** `skills/active-testing/replay/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Replay Capability.

---

# Operation: replay

## Request

```yaml
replay:
  target:
  recording_ref:
  adjustments:
  bounds:
    max_requests:
    rate_ceiling:
  scope_id:
  roe_id:
```

`target` SHALL be an in-scope endpoint. `recording_ref` references a recorded traffic Artifact.
`adjustments` specifies bounded field changes. `bounds` limits volume and rate.

## Response

```yaml
replay_result:
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
- `recording_ref` SHALL resolve to a recorded traffic Artifact.
- `max_requests` SHALL be a positive integer when present.

---

# Postconditions

- Every delivery SHALL have been policy-gated.
- Replay SHALL have remained non-destructive and bounded.
- No out-of-scope target SHALL have been contacted.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `replay` operation is stable. Additional adjustment modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
