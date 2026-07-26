# HTTP Archive Examples

**File:** `skills/evidence/http-archive/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the HTTP Archive Capability.

---

# Example 1 — Archive A Session As HAR

## Request

```yaml
archive:
  target: https://app.example.com
  selection:
    session: session-2201
  bounds:
    max_transactions: 300
  redaction:
    redact_credentials: true
    redact_tokens: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
archive_result:
  target: https://app.example.com
  artifact_ref: artifact-ev-9101
  transaction_count: 214
  evidence_ref: evidence-ev-8101
  metrics_ref: metrics-ev-7101
  decision_summary:
    allow: 214
    denied: 0
```

The capability archives a bounded, redacted set of HTTP transactions as a `http-archive` Artifact
and invokes the shared Evidence lifecycle to promote it.

---

# Example 2 — Requires Approval

## Request

```yaml
archive:
  target: https://admin.example.com
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
archive_result:
  target: https://admin.example.com
  metrics_ref: metrics-ev-7102
  decision_summary:
    allow: 0
    awaiting_approval: 1
```

The Rules of Engagement require approval before archiving this host; the capability defers.

---

# Example 3 — Out Of Scope Rejected

## Request

```yaml
archive:
  target: https://out-of-scope.example.net/
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
archive_result:
  target: https://out-of-scope.example.net/
  decision_summary:
    denied: 1
```

The target is out of scope, so the capability rejects the request.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
