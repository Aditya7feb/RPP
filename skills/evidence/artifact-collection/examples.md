# Artifact Collection Examples

**File:** `skills/evidence/artifact-collection/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Artifact Collection
Capability.

---

# Example 1 — Collect A Certificate

## Request

```yaml
collect:
  sources:
    - store://collected/cert-app-example
  types:
    - certificate
  bounds:
    max_artifacts: 10
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  artifact_refs:
    - artifact-ev-9301
  artifact_count: 1
  evidence_refs:
    - evidence-ev-8301
  metrics_ref: metrics-ev-7301
```

The capability collects a certificate artifact referencing the Certificate schema and invokes the
shared Evidence lifecycle to promote it.

---

# Example 2 — Collect Files

## Request

```yaml
collect:
  sources:
    - store://collected/downloads
  types:
    - file
  bounds:
    max_artifacts: 100
    max_size_bytes: 10485760
  redaction:
    redact_sensitive: true
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  artifact_refs:
    - artifact-ev-9302
  artifact_count: 24
  evidence_refs:
    - evidence-ev-8302
  metrics_ref: metrics-ev-7302
```

The capability collects bounded file artifacts and promotes them through the shared Evidence
lifecycle.

---

# Example 3 — Unauthorized Location Rejected

## Request

```yaml
collect:
  sources:
    - store://unauthorized/path
  scope_id: scope-example-2024
  roe_id: roe-example-2024
```

## Response

```yaml
collect_result:
  artifact_refs: []
  artifact_count: 0
  reason: unauthorized-location
```

The source is outside authorized locations, so the capability rejects collection.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
