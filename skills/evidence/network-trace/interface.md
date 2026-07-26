# Network Trace Interface

**File:** `skills/evidence/network-trace/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Network Trace
Capability.

---

# Operation: trace

## Request

```yaml
trace:
  target:
  selection:
    protocols:
    ports:
  bounds:
    max_flows:
    max_duration:
  redaction:
  scope_id:
  roe_id:
```

`target` SHALL be an in-scope host or service. `selection` selects protocols and ports. `bounds`
limits capture.

## Response

```yaml
trace_result:
  target:
  artifact_ref:
  flow_count:
  evidence_ref:
  metrics_ref:
  decision_summary:
```

`artifact_ref` references an [Artifact](../../../schemas/artifact.md) of type `network-trace`;
`evidence_ref` references [Evidence](../../../schemas/evidence.md) produced through the shared
lifecycle; `metrics_ref` references [Metrics](../../../schemas/metrics.md). No Findings or Risk are
produced.

---

# Preconditions

- `target` SHALL be within the assessment [Scope](../../../schemas/scope.md).
- The [Policy Engine](../../shared/policy-engine/README.md) SHALL be available.
- `max_flows` SHALL be a positive integer when present.

---

# Postconditions

- Capture SHALL have been policy-gated and bounded.
- Sensitive payload content SHALL have been redacted where configured.
- No out-of-scope traffic SHALL have been captured.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `trace` operation is stable. Additional selection and capture modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
