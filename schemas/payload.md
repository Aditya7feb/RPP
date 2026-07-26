# Payload Schema

**File:** `schemas/payload.md`

**Version:** 1.0.0

---

# Purpose

The Payload Schema defines the canonical, implementation-independent representation of a
test input generated for use during an assessment within the Robust PenTest Platform
(RPP).

A Payload is a structured, reusable description of an input to be delivered to a target by
an active-testing or domain capability. Payloads describe **what will be sent**, by
reference and intent, before delivery.

A Payload represents configuration and data only. It SHALL NOT contain security
interpretation, findings, risk, or secrets. Interpretation of a target's response to a
Payload is deferred to domain capabilities.

---

# Design Principles

A Payload SHALL be

- Declarative and reusable
- Traceable to its generating capability and source
- Non-destructive by default
- Referenced rather than inlined for large or sensitive content
- Immutable once recorded
- Auditable
- Implementation independent

---

# Identity

Every Payload SHALL contain

```yaml
payload_id:

schema_version:
```

`payload_id` SHALL be unique within an assessment. `schema_version` SHALL be `1.0.0`.

---

# Classification

Every Payload SHALL contain

```yaml
classification:
  category:
  intent:
  encoding:
```

`category` SHALL name the payload class, such as `injection`, `traversal`, `fuzz`,
`overflow-marker`, `oob-marker`, or `benign-probe`. `intent` SHALL describe the input's
purpose, such as `boundary-test` or `marker-detection`. `encoding` SHALL name the applied
encoding, such as `none`, `url`, `base64`, or `html-entity`.

---

# Content

Every Payload SHALL contain

```yaml
content:
  template_ref:
  value_ref:
  variables:
```

`template_ref` MAY reference a payload template. `value_ref` SHALL reference the concrete
payload value by reference; large or sensitive values SHALL NOT be inlined. `variables`
SHALL be a namespaced map of template variable bindings. Marker and out-of-band values
SHALL be referenced, never inlined.

---

# Lineage

A Payload MAY contain

```yaml
lineage:
  source:
  base_payload_id:
  mutation_ref:
```

`source` SHALL name the origin, such as `wordlist`, `generated`, `mutated`, or `mined`.
`base_payload_id` MAY reference the Payload from which this one was derived.
`mutation_ref` MAY reference the mutation that produced it.

---

# Safety

Every Payload SHALL contain

```yaml
safety:
  non_destructive: true
  requires_approval:
```

`non_destructive` SHALL default to `true`. A Payload whose delivery could alter or damage
target state SHALL set `requires_approval` to `true` so that delivery is gated by the
Policy Engine.

---

# Required Fields

A Payload SHALL define `payload_id`, `schema_version`, `classification.category`,
`content.value_ref`, and `safety.non_destructive`.

---

# Validation Rules

- `payload_id` SHALL be unique within an assessment.
- `schema_version` SHALL follow semantic versioning.
- `content.value_ref` SHALL resolve to a stored value; it SHALL NOT be inlined for
  sensitive content.
- Marker, out-of-band, and credential values SHALL be referenced, never inlined.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Relationships

- A Payload MAY be delivered by an active-testing capability that records
  [Observations](observation.md) and [Artifacts](artifact.md).
- A Payload MAY derive from another Payload through `lineage`.
- A Payload SHALL NOT reference [Findings](finding.md) or [Risk](risk.md); interpretation
  belongs to domain capabilities.

---

# Example Object

```yaml
payload_id: payload-4001
schema_version: 1.0.0
classification:
  category: fuzz
  intent: boundary-test
  encoding: url
content:
  template_ref: template-boundary-default
  value_ref: payload-value-4001
  variables:
    length: 2048
lineage:
  source: mutated
  base_payload_id: payload-3990
  mutation_ref: mutation-1207
safety:
  non_destructive: true
  requires_approval: false
```

---

# Extension Points

- Additional `classification.category` values MAY be introduced.
- `content` MAY be extended with additional template metadata.
- Consumers SHALL ignore unknown optional fields.

---

# Versioning Notes

`schema_version` SHALL follow semantic versioning. Backward-compatible additions increment
the minor version. Unknown optional fields SHALL be ignored by consumers.
