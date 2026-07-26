# Log Collection Examples

**File:** `skills/evidence/log-collection/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Log Collection Capability.

---

# Example 1 — Collect Application Logs In A Window

## Request

```yaml
collect:
  sources:
    - log-source://app.example.com/application
  window:
    start: "2026-07-26T14:00:00Z"
    end: "2026-07-26T14:30:00Z"
  bounds:
    max_events: 5000
  redaction:
    redact_sensitive: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  artifact_ref: artifact-ev-9401
  event_count: 3120
  evidence_ref: evidence-ev-8401
  metrics_ref: metrics-ev-7401
```

The capability collects an ordered, redacted window of application log events as a `log-collection`
Artifact and invokes the shared Evidence lifecycle to promote it.

---

# Example 2 — Bounds Reached

## Request

```yaml
collect:
  sources:
    - log-source://svc.example.com/service
  bounds:
    max_events: 1000
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  artifact_ref: artifact-ev-9402
  event_count: 1000
  evidence_ref: evidence-ev-8402
  metrics_ref: metrics-ev-7402
```

Collection bounds are reached, so the capability finalizes a partial, ordered collection.

---

# Example 3 — Unauthorized Source Rejected

## Request

```yaml
collect:
  sources:
    - log-source://unauthorized/source
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  event_count: 0
  reason: unauthorized-source
```

The source is outside authorized sources, so the capability rejects collection.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
