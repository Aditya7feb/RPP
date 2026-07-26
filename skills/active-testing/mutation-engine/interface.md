# Mutation Engine Interface

**File:** `skills/active-testing/mutation-engine/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Mutation
Engine Capability.

---

# Operation: mutate

## Request

```yaml
mutate:
  base_payload_ref:
  strategies:
  bounds:
    max_variants:
  seed:
```

`base_payload_ref` references the base [Payload](../../../schemas/payload.md). `strategies`
names mutation strategies. `bounds.max_variants` limits output. `seed` enables deterministic
reproduction.

## Response

```yaml
mutate_result:
  base_payload_ref:
  variant_refs:
  variant_count:
  metrics_ref:
```

`variant_refs` reference derived [Payloads](../../../schemas/payload.md); `metrics_ref`
references [Metrics](../../../schemas/metrics.md).

---

# Preconditions

- `base_payload_ref` SHALL resolve to a Payload.
- `max_variants` SHALL be a positive integer when present.

---

# Postconditions

- Output SHALL be bounded by `max_variants`.
- Each variant SHALL carry lineage and safety markers.
- No target SHALL have been contacted and no Findings or Risk produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `mutate` operation is stable. Additional strategies MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
