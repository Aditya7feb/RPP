# Timeline Interface

**File:** `skills/evidence/timeline/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Timeline Capability.

---

# Operation: correlate

## Request

```yaml
correlate:
  observation_refs:
  evidence_refs:
  correlation:
    causal_links:
  bounds:
    max_items:
```

`observation_refs` and `evidence_refs` reference items to correlate. `correlation` configures causal
linking. `bounds` limits timeline size.

## Response

```yaml
correlate_result:
  timeline_artifact_ref:
  correlated_count:
  evidence_ref:
  metrics_ref:
```

`timeline_artifact_ref` references a timeline [Artifact](../../../schemas/artifact.md);
`evidence_ref` references [Evidence](../../../schemas/evidence.md) produced through the shared
lifecycle; `metrics_ref` references [Metrics](../../../schemas/metrics.md). No Findings or Risk are
produced, and no security interpretation is included.

---

# Preconditions

- `observation_refs` and `evidence_refs` SHALL reference existing canonical objects.
- `max_items` SHALL be a positive integer when present.

---

# Postconditions

- The timeline SHALL preserve chronology and causal relationships.
- The timeline SHALL reference canonical objects by ID without duplicating content.
- No interpretation, Finding, or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `correlate` operation is stable. Additional correlation modes MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
