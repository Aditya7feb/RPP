# Traffic Comparison Interface

**File:** `skills/active-testing/traffic-comparison/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Traffic Comparison
Capability.

---

# Operation: compare

## Request

```yaml
compare:
  baseline_ref:
  candidate_ref:
  comparison:
    dimensions:
  bounds:
    max_transactions:
```

`baseline_ref` and `candidate_ref` reference recorded traffic Artifacts. `comparison.dimensions`
selects compared dimensions, such as `status`, `headers`, `timing`, and `body`. `bounds` limits
comparison scope.

## Response

```yaml
compare_result:
  diff_artifact_ref:
  difference_count:
  metrics_ref:
```

`diff_artifact_ref` references a difference [Artifact](../../../schemas/artifact.md);
`metrics_ref` references [Metrics](../../../schemas/metrics.md). No Findings or Risk are
produced.

---

# Preconditions

- `baseline_ref` and `candidate_ref` SHALL resolve to recorded traffic Artifacts.
- `max_transactions` SHALL be a positive integer when present.

---

# Postconditions

- The difference Artifact SHALL have sensitive content redacted.
- No target SHALL have been contacted.
- No Findings or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `compare` operation is stable. Additional comparison dimensions MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
