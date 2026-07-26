# Log Collection Interface

**File:** `skills/evidence/log-collection/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Log Collection
Capability.

---

# Operation: collect

## Request

```yaml
collect:
  sources:
  window:
    start:
    end:
  bounds:
    max_events:
  redaction:
  scope_id:
  roe_id:
```

`sources` reference authorized log sources. `window` bounds the time range. `bounds` limits volume.

## Response

```yaml
collect_result:
  artifact_ref:
  event_count:
  evidence_ref:
  metrics_ref:
```

`artifact_ref` references an [Artifact](../../../schemas/artifact.md) of type `log-collection`;
`evidence_ref` references [Evidence](../../../schemas/evidence.md) produced through the shared
lifecycle; `metrics_ref` references [Metrics](../../../schemas/metrics.md). No Findings or Risk are
produced.

---

# Preconditions

- `sources` SHALL reference authorized sources within the assessment
  [Scope](../../../schemas/scope.md).
- `max_events` SHALL be a positive integer when present.

---

# Postconditions

- Only authorized sources SHALL have been collected.
- Log ordering SHALL have been preserved.
- Sensitive content SHALL have been redacted where configured.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `collect` operation is stable. Additional selection modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
