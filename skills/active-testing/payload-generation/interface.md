# Payload Generation Interface

**File:** `skills/active-testing/payload-generation/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Payload
Generation Capability.

---

# Operation: generate

## Request

```yaml
generate:
  template_ref:
  seeds:
    wordlist_name:
    max_entries:
  mutation:
    strategies:
    max_variants:
    seed:
  encoding:
  bounds:
    max_payloads:
```

`template_ref` references a template. `seeds` draws from a wordlist. `mutation` derives
variants. `encoding` selects an encoding. `bounds` limits output.

## Response

```yaml
generate_result:
  payload_refs:
  payload_count:
  metrics_ref:
```

`payload_refs` reference generated [Payloads](../../../schemas/payload.md); `metrics_ref`
references [Metrics](../../../schemas/metrics.md).

---

# Preconditions

- `template_ref` SHALL resolve when provided.
- Referenced wordlists and mutation strategies SHALL resolve.
- `max_payloads` SHALL be a positive integer when present.

---

# Postconditions

- Output SHALL be bounded by `max_payloads`.
- Each Payload SHALL carry lineage and safety markers.
- No target SHALL have been contacted and no Findings or Risk produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `generate` operation is stable. Additional composition inputs MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
