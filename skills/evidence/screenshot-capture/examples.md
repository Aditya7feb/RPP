# Screenshot Capture Examples

**File:** `skills/evidence/screenshot-capture/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Screenshot Capture
Capability.

---

# Example 1 — Full-Page Capture

## Request

```yaml
capture:
  target: https://app.example.com/dashboard
  options:
    full_page: true
  redaction:
    redact_sensitive: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
capture_result:
  target: https://app.example.com/dashboard
  artifact_ref: artifact-ev-9001
  evidence_ref: evidence-ev-8001
  metrics_ref: metrics-ev-7001
  decision_summary:
    allow: 1
    denied: 0
```

The capability renders and captures the page, records it as a `screenshot` Artifact, and invokes
the shared Evidence lifecycle to promote it into durable Evidence.

---

# Example 2 — Requires Approval

## Request

```yaml
capture:
  target: https://admin.example.com/console
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
capture_result:
  target: https://admin.example.com/console
  metrics_ref: metrics-ev-7002
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The Rules of Engagement require approval before capturing this page; the capability defers.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
capture:
  target: https://out-of-scope.example.net/
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
capture_result:
  target: https://out-of-scope.example.net/
  decision_summary:
    denied: 1
```

The target is out of scope, so the capability rejects the capture.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
