# Observation Schema

**File:** `schemas/observation.md`

**Version:** 1.0.0

---

# Purpose

The Observation Schema defines the canonical, implementation-independent
representation of a raw signal captured during an assessment within the Robust
PenTest Platform (RPP).

An Observation is the first stage of the canonical assessment pipeline. It
records **what was seen** before any validation or interpretation. Observations
are promoted into [Evidence](evidence.md) once corroborated, analyzed to produce
[Findings](finding.md), scored as [Risk](risk.md), and translated into
recommendations.

The canonical pipeline is

```
Observation → Evidence → Analysis → Finding → Risk → Recommendation
```

An Observation represents a captured signal only. It SHALL NOT contain security
interpretation, findings, risk, or secrets. Interpretation is deferred to later
pipeline stages.

---

# Design Principles

An Observation SHALL be

- Raw and pre-interpretation
- Traceable to its source capability
- Immutable once recorded
- Confidence-graded
- Linkable to Assets and Evidence
- Auditable
- Implementation independent

---

# Identity

Every Observation SHALL contain

```yaml
observation_id:

assessment_id:

task_id:

schema_version:
```

`observation_id` SHALL be unique within an assessment.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`task_id` SHALL reference the [task](task.md) during which the Observation was
captured.

`schema_version` SHALL be `1.0.0`.

---

# Source

Every Observation SHALL contain

```yaml
source:
```

`source` SHALL contain

```yaml
capability:

layer:

operation:
```

`capability` SHALL identify the capability that captured the Observation.

`layer` SHALL identify the architectural layer, such as `shared` or `discovery`.

`operation` SHALL identify the operation that produced the signal.

---

# Classification

Every Observation SHALL contain

```yaml
type:

observed_at:
```

`type` SHALL describe the signal category, such as `dns-record`, `open-port`,
`http-response`, `tls-certificate`, or `banner`.

`observed_at` SHALL be the time the signal was captured.

---

# Subject

Every Observation SHALL contain

```yaml
subject:
```

`subject` SHALL contain

```yaml
target:

asset_id:
```

`target` SHALL identify the entity the signal concerns, such as a host, URL, or
address.

`asset_id` MAY reference the [Asset](asset.md) the Observation contributes to,
where one has been established.

---

# Content

Every Observation SHALL contain

```yaml
content:
```

`content` SHALL contain

```yaml
summary:

data_ref:

attributes:
```

`summary` SHALL be a short, non-sensitive description of the signal.

`data_ref` SHALL reference the raw captured data stored as an artifact rather
than inlined for large payloads.

`attributes` SHALL be a namespaced map of observed facts.

`content` SHALL contain observed facts only and SHALL NOT contain security
interpretation. Secrets SHALL be redacted before an Observation is recorded.

---

# Confidence

Every Observation SHALL contain

```yaml
confidence:
```

`confidence` SHALL be one of `Low`, `Medium`, `High`, or `Verified` and SHALL be
calculated according to [the confidence model](../skills/core/confidence-model.md).

Confidence measures certainty that the signal was captured correctly, not that a
weakness exists.

---

# Promotion

An Observation MAY contain

```yaml
evidence:
```

`evidence` SHALL be an array of [evidence](evidence.md) references produced when
the Observation is corroborated and promoted.

An Observation without evidence references remains a raw, uncorroborated signal.

---

# Extensions

An Observation MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Observation object SHALL contain

- `observation_id`
- `assessment_id`
- `task_id`
- `schema_version`
- `source.capability`
- `type`
- `observed_at`
- `subject.target`
- `content.summary`
- `confidence`

---

# Validation Rules

A valid Observation object SHALL satisfy

- `confidence` is one of the allowed confidence values
- `content` contains observed facts only, without interpretation
- Large raw data is referenced through `data_ref`, not inlined
- `asset_id`, when present, references an existing Asset in the assessment
- `evidence`, when present, references existing Evidence in the assessment
- No secret material appears in `content` or `extensions`

---

# Relationships To Other Schemas

```
Observation (raw signal)

↓ corroboration

Evidence (immutable record)

↓ analysis

Finding (interpreted weakness)

↓ scoring

Risk

↓ translation

Recommendation
```

An Observation belongs to exactly one [assessment](assessment.md) and
[task](task.md). It MAY contribute to an [Asset](asset.md) and is promoted into
[Evidence](evidence.md), which is analyzed into [Findings](finding.md) and scored
as [Risk](risk.md).

---

# Example Object

```yaml
observation_id: obs-1201
assessment_id: asmt-42
task_id: task-port-discovery
schema_version: 1.0.0
source:
  capability: port-discovery
  layer: discovery
  operation: probe-port
type: open-port
observed_at: 2026-07-25T18:39:00Z
subject:
  target: 93.184.216.34:443
  asset_id: asset-0007
content:
  summary: TCP port 443 responded with a TLS service
  data_ref: artifact://obs/1201-banner
  attributes:
    protocol: https
    state: open
confidence: High
evidence:
  - evidence-tcp-0007
extensions: {}
```

---

# Extension Points

- New `type` values MAY be introduced for emerging signal categories.
- New `attributes` keys MAY be added without a schema change.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields or additional observation types.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
