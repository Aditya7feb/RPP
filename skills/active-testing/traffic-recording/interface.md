# Traffic Recording Interface

**File:** `skills/active-testing/traffic-recording/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Traffic Recording
Capability.

---

# Operation: record

## Request

```yaml
record:
  scope_selector:
  bounds:
    max_transactions:
    max_duration:
  redaction:
  scope_id:
  roe_id:
```

`scope_selector` selects in-scope exchanges. `bounds` limits capture. `redaction` configures
sensitive-content removal.

## Response

```yaml
record_result:
  artifact_refs:
  transaction_count:
  metrics_ref:
  decision_summary:
```

`artifact_refs` reference [Artifacts](../../../schemas/artifact.md); `metrics_ref` references
[Metrics](../../../schemas/metrics.md). No Findings or Risk are produced.

---

# Preconditions

- The selected exchanges SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- `max_transactions` SHALL be a positive integer when present.

---

# Postconditions

- Recording SHALL have been authorized and bounded.
- Stored artifacts SHALL have sensitive content redacted.
- No out-of-scope traffic SHALL have been recorded.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `record` operation is stable. Additional selectors and redaction modes MAY be introduced in
a backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
