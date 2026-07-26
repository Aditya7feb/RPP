# HTTP Archive Interface

**File:** `skills/evidence/http-archive/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the HTTP Archive
Capability.

---

# Operation: archive

## Request

```yaml
archive:
  target:
  selection:
  bounds:
    max_transactions:
  redaction:
  scope_id:
  roe_id:
```

`target` SHALL be an in-scope endpoint. `selection` selects transactions. `bounds` limits volume.
`redaction` configures content removal.

## Response

```yaml
archive_result:
  target:
  artifact_ref:
  transaction_count:
  evidence_ref:
  metrics_ref:
  decision_summary:
```

`artifact_ref` references an [Artifact](../../../schemas/artifact.md) of type `http-archive`;
`evidence_ref` references [Evidence](../../../schemas/evidence.md) produced through the shared
lifecycle; `metrics_ref` references [Metrics](../../../schemas/metrics.md). No Findings or Risk are
produced.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- `max_transactions` SHALL be a positive integer when present.

---

# Postconditions

- Every request SHALL have been policy-gated.
- Sensitive content SHALL have been redacted.
- No out-of-scope traffic SHALL have been archived.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `archive` operation is stable. Additional selection and redaction modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
