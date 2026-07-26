# Screenshot Capture Interface

**File:** `skills/evidence/screenshot-capture/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Screenshot Capture
Capability.

---

# Operation: capture

## Request

```yaml
capture:
  target:
  options:
    full_page:
    viewport:
  redaction:
  scope_id:
  roe_id:
```

`target` SHALL be an in-scope page. `options` select capture parameters. `redaction` configures
on-screen content removal.

## Response

```yaml
capture_result:
  target:
  artifact_ref:
  evidence_ref:
  metrics_ref:
  decision_summary:
```

`artifact_ref` references an [Artifact](../../../schemas/artifact.md); `evidence_ref` references
[Evidence](../../../schemas/evidence.md) produced through the shared lifecycle; `metrics_ref`
references [Metrics](../../../schemas/metrics.md). No Findings or Risk are produced.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.

---

# Postconditions

- Capture SHALL have been policy-gated.
- Sensitive on-screen content SHALL have been redacted where configured.
- No out-of-scope page SHALL have been captured.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `capture` operation is stable. Additional capture options MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
