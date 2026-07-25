# Risk Schema

**File:** `schemas/risk.md`

**Version:** 1.0.0

---

# Purpose

The Risk Schema defines the canonical, implementation-independent representation
of the risk associated with a [Finding](finding.md) within the Robust PenTest
Platform (RPP).

Risk is a first-class object in the canonical assessment pipeline. It expresses
the business exposure a Finding represents, derived from likelihood and impact,
so that risk is modelled consistently rather than embedded ad hoc inside
Findings.

The canonical pipeline is

```
Observation → Evidence → Analysis → Finding → Risk → Recommendation
```

A Risk object represents scored interpretation only. It SHALL NOT contain raw
signals, evidence payloads, or secrets. It references the Finding it scores.

---

# Design Principles

A Risk SHALL be

- Derived from a Finding
- Composed of likelihood and impact
- Deterministic given the same inputs
- Traceable and auditable
- Aggregatable to asset and assessment level
- Implementation independent

---

# Identity

Every Risk SHALL contain

```yaml
risk_id:

assessment_id:

finding_id:

schema_version:
```

`risk_id` SHALL be unique within an assessment.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`finding_id` SHALL reference the [Finding](finding.md) this Risk scores.

`schema_version` SHALL be `1.0.0`.

---

# Likelihood

Every Risk SHALL contain

```yaml
likelihood:
```

`likelihood` SHALL contain

```yaml
rating:

factors:
```

`rating` SHALL be one of `Low`, `Medium`, `High`, or `Critical`.

`factors` SHALL enumerate the contributing considerations, such as
`exposure`, `exploit_availability`, `authentication_required`, and
`attack_complexity`.

Likelihood measures the probability that the weakness is exploited.

---

# Impact

Every Risk SHALL contain

```yaml
impact:
```

`impact` SHALL contain

```yaml
rating:

dimensions:
```

`rating` SHALL be one of `Low`, `Medium`, `High`, or `Critical`.

`dimensions` SHALL describe the affected concerns, such as `confidentiality`,
`integrity`, `availability`, and `business_function`.

Impact measures the consequence if the weakness is exploited.

---

# Score

Every Risk SHALL contain

```yaml
score:
```

`score` SHALL contain

```yaml
model:

value:

severity:

vector:
```

`model` SHALL identify the scoring model, such as `likelihood-impact` or `cvss`.

`value` SHALL be the numeric or normalized score produced by the model.

`severity` SHALL be one of `Informational`, `Low`, `Medium`, `High`, or
`Critical`, mapping the score to the canonical severity scale used by
[Findings](finding.md).

`vector`, when the model is `cvss`, SHALL carry the CVSS vector string.

The mapping from `score.value` to `score.severity` SHALL be deterministic.

---

# Business Context

A Risk MAY contain

```yaml
business_context:
```

`business_context` SHALL contain

```yaml
asset_criticality:

data_sensitivity:

exposure:
```

Business context adjusts likelihood and impact according to the value of the
affected [Asset](asset.md) and its exposure.

Business context SHALL be optional and SHALL NOT be fabricated when unknown.

---

# Aggregation

A Risk MAY contain

```yaml
aggregation:
```

`aggregation` SHALL contain

```yaml
asset_id:

contributes_to_asset_risk:

contributes_to_assessment_risk:
```

`asset_id` SHALL reference the [Asset](asset.md) whose aggregated risk this Risk
contributes to.

Aggregation enables asset-level and assessment-level risk rollups without
duplicating per-Finding risk.

---

# Extensions

A Risk MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Risk object SHALL contain

- `risk_id`
- `assessment_id`
- `finding_id`
- `schema_version`
- `likelihood.rating`
- `impact.rating`
- `score.model`
- `score.value`
- `score.severity`

---

# Validation Rules

A valid Risk object SHALL satisfy

- `finding_id` references an existing Finding in the assessment
- `likelihood.rating` and `impact.rating` are allowed ratings
- `score.severity` is a canonical severity value
- The mapping from `score.value` to `score.severity` is deterministic
- `score.vector` is present when `score.model` is `cvss`
- `aggregation.asset_id`, when present, references an existing Asset
- No secret material appears in `extensions`

---

# Relationships To Other Schemas

```
Finding

└── Risk (scores the finding)

     ├── composed of Likelihood and Impact
     ├── mapped to canonical Severity
     ├── adjusted by Business Context (Asset criticality)
     └── aggregated to Asset and Assessment risk
```

A Risk belongs to exactly one [assessment](assessment.md) and scores exactly one
[Finding](finding.md). It references the affected [Asset](asset.md) for
aggregation and maps to the canonical severity scale shared with Findings.

---

# Example Object

```yaml
risk_id: risk-0007
assessment_id: asmt-42
finding_id: finding-tls-0007
schema_version: 1.0.0
likelihood:
  rating: Medium
  factors:
    - exposure: internet-facing
    - authentication_required: false
    - attack_complexity: low
impact:
  rating: High
  dimensions:
    - confidentiality
    - integrity
score:
  model: cvss
  value: 7.4
  severity: High
  vector: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"
business_context:
  asset_criticality: high
  data_sensitivity: sensitive
  exposure: internet-facing
aggregation:
  asset_id: asset-0007
  contributes_to_asset_risk: true
  contributes_to_assessment_risk: true
extensions: {}
```

---

# Extension Points

- New scoring `model` values MAY be introduced with deterministic severity
  mappings.
- New likelihood or impact factors MAY be added without a schema change.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields or additional scoring models.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
