# Replay Examples

**File:** `skills/active-testing/replay/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Replay Capability.

---

# Example 1 — Deterministic Replay

## Request

```yaml
replay:
  target: https://app.example.com
  recording_ref: artifact-8401
  bounds:
    max_requests: 200
    rate_ceiling: 10
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
replay_result:
  target: https://app.example.com
  observations:
    - id: obs-rp-4001
      kind: replay-response
      detail: response recorded for interpretation
  artifact_refs:
    - artifact-8501
  metrics_ref: metrics-9701
  decision_summary:
    allow: 200
    denied: 0
```

The capability reconstructs and re-delivers recorded requests, recording responses for domain
skills to interpret. It emits no Findings.

---

# Example 2 — State-Changing Adjustment Requires Approval

## Request

```yaml
replay:
  target: https://app.example.com
  recording_ref: artifact-8401
  adjustments:
    method: DELETE
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
replay_result:
  target: https://app.example.com
  observations: []
  metrics_ref: metrics-9702
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The adjustment could alter target state, so delivery is deferred pending approval.

---

# Example 3 — Missing Recording Rejected

## Request

```yaml
replay:
  target: https://app.example.com
  recording_ref: artifact-nonexistent
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
replay_result:
  target: https://app.example.com
  observations: []
  decision_summary:
    rejected: 1
  reason: recording-unavailable
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
