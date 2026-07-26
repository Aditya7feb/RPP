# Traffic Recording Examples

**File:** `skills/active-testing/traffic-recording/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Traffic Recording
Capability.

---

# Example 1 — Record A Bounded Session

## Request

```yaml
record:
  scope_selector:
    host: app.example.com
  bounds:
    max_transactions: 300
    max_duration: 120s
  redaction:
    redact_credentials: true
    redact_tokens: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
record_result:
  artifact_refs:
    - artifact-8401
  transaction_count: 214
  metrics_ref: metrics-9601
  decision_summary:
    allow: 1
    denied: 0
```

The capability records a bounded, redacted session as a `traffic-recording` Artifact.

---

# Example 2 — Requires Approval

## Request

```yaml
record:
  scope_selector:
    host: admin.example.com
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
record_result:
  artifact_refs: []
  metrics_ref: metrics-9602
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The Rules of Engagement require approval before recording this host; the capability defers.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
record:
  scope_selector:
    host: out-of-scope.example.net
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
record_result:
  artifact_refs: []
  decision_summary:
    denied: 1
```

The selected host is out of scope, so the capability rejects the request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
