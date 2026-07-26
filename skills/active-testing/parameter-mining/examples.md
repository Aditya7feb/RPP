# Parameter Mining Examples

**File:** `skills/active-testing/parameter-mining/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Parameter Mining
Capability.

---

# Example 1 — Discover Query Parameters

## Request

```yaml
mine:
  target: https://app.example.com/search
  locations:
    - query
  candidate_source:
    wordlist_name: common-parameters
    max_candidates: 500
  bounds:
    max_requests: 600
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
mine_result:
  target: https://app.example.com/search
  observations:
    - id: obs-pm-4001
      kind: parameter-accepted
      detail: reflected query parameter observed
  artifact_refs:
    - artifact-8201
  metrics_ref: metrics-9401
  decision_summary:
    allow: 512
    denied: 0
```

The capability reports an accepted, reflected query parameter as an Observation. Whether it is
exploitable is left to domain skills.

---

# Example 2 — Requires Approval

## Request

```yaml
mine:
  target: https://app.example.com/admin
  locations:
    - query
    - header
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
mine_result:
  target: https://app.example.com/admin
  observations: []
  metrics_ref: metrics-9402
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The Rules of Engagement require approval before probing this path; the capability defers.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
mine:
  target: https://out-of-scope.example.net/
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
mine_result:
  target: https://out-of-scope.example.net/
  observations: []
  decision_summary:
    denied: 1
```

The target is out of scope, so the capability rejects the request before any probe.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
