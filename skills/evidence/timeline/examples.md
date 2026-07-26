# Timeline Examples

**File:** `skills/evidence/timeline/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Timeline Capability.

---

# Example 1 — Correlate Observations And Evidence

## Request

```yaml
correlate:
  observation_refs:
    - obs-fz-4001
    - obs-rp-4001
  evidence_refs:
    - evidence-ev-8101
    - evidence-ev-8201
  correlation:
    causal_links: true
  bounds:
    max_items: 500
```

## Response

```yaml
correlate_result:
  timeline_artifact_ref: artifact-ev-9501
  correlated_count: 4
  evidence_ref: evidence-ev-8501
  metrics_ref: metrics-ev-7501
```

The capability orders and correlates the referenced Observations and Evidence into a chronological
timeline Artifact, preserving causal relationships. It references items by ID and performs no
interpretation.

---

# Example 2 — Partial Timeline On Missing Reference

## Request

```yaml
correlate:
  observation_refs:
    - obs-fz-4001
    - obs-missing-0000
  evidence_refs:
    - evidence-ev-8101
```

## Response

```yaml
correlate_result:
  timeline_artifact_ref: artifact-ev-9502
  correlated_count: 2
  evidence_ref: evidence-ev-8502
  metrics_ref: metrics-ev-7502
```

One referenced Observation could not be resolved, so the capability produces a partial timeline over
the resolvable subset.

---

# Example 3 — Correlation Only (No Interpretation)

## Result

```yaml
correlate_result:
  timeline_artifact_ref: artifact-ev-9503
  correlated_count: 12
  metrics_ref: metrics-ev-7503
```

The timeline records chronology and causal relationships only. It contains no vulnerability
inference, Finding classification, Risk prioritization, or security analysis; interpretation is left
to Domain Security capabilities.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
