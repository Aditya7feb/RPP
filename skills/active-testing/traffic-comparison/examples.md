# Traffic Comparison Examples

**File:** `skills/active-testing/traffic-comparison/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Traffic Comparison
Capability.

---

# Example 1 — Baseline Versus Replay

## Request

```yaml
compare:
  baseline_ref: artifact-8401
  candidate_ref: artifact-8501
  comparison:
    dimensions:
      - status
      - headers
      - body
  bounds:
    max_transactions: 200
```

## Response

```yaml
compare_result:
  diff_artifact_ref: artifact-8601
  difference_count: 12
  metrics_ref: metrics-9801
```

The capability compares a baseline recording with a replayed recording and emits a structured
`traffic-diff` Artifact. Whether the differences are significant is left to domain skills.

---

# Example 2 — Timing-Only Comparison With Tolerance

## Request

```yaml
compare:
  baseline_ref: artifact-8401
  candidate_ref: artifact-8501
  comparison:
    dimensions:
      - timing
  bounds:
    max_transactions: 200
```

## Response

```yaml
compare_result:
  diff_artifact_ref: artifact-8602
  difference_count: 3
  metrics_ref: metrics-9802
```

Timing differences below the configured threshold are ignored; only significant variations are
recorded in the difference Artifact.

---

# Example 3 — Missing Recording Rejected

## Request

```yaml
compare:
  baseline_ref: artifact-8401
  candidate_ref: artifact-nonexistent
```

## Response

```yaml
compare_result:
  outcome: rejected
  reason: recording-unavailable
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
