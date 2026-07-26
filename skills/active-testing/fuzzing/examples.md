# Fuzzing Examples

**File:** `skills/active-testing/fuzzing/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Fuzzing Capability.

---

# Example 1 — Bounded Parameter Fuzzing

## Request

```yaml
fuzz:
  target: https://app.example.com/search
  surface:
    parameter: q
    location: query
  corpus_ref: corpus-4301
  bounds:
    max_requests: 500
    rate_ceiling: 10
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
fuzz_result:
  target: https://app.example.com/search
  observations:
    - id: obs-fz-4001
      kind: response-anomaly
      detail: status and length variation recorded for interpretation
  artifact_refs:
    - artifact-8301
  metrics_ref: metrics-9501
  decision_summary:
    allow: 500
    denied: 0
```

The capability delivers a bounded corpus and records response variation as Observations for
domain skills to interpret. It emits no Findings.

---

# Example 2 — Payload Requires Approval

## Request

```yaml
fuzz:
  target: https://app.example.com/account
  surface:
    parameter: action
    location: body
  corpus_ref: corpus-4500
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
fuzz_result:
  target: https://app.example.com/account
  observations: []
  metrics_ref: metrics-9502
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The corpus contains payloads marked `requires_approval`; delivery is deferred pending approval.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
fuzz:
  target: https://out-of-scope.example.net/
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
fuzz_result:
  target: https://out-of-scope.example.net/
  observations: []
  decision_summary:
    denied: 1
```

The target is out of scope, so the capability rejects the request before any delivery.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
