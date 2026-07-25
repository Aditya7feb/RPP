# Asset Relationship Schema

**File:** `schemas/asset-relationship.md`

**Version:** 1.0.0

---

# Purpose

The Asset Relationship Schema defines the canonical, implementation-independent
representation of a typed connection between two [Assets](asset.md) within the
Robust PenTest Platform (RPP).

Asset Relationships express how discovered entities relate to one another — for
example, that a subdomain `resolves-to` a host, that a host `exposes` a service,
or that a service `serves` a web application. Together, Assets and Asset
Relationships form the canonical asset graph of an assessment.

An Asset Relationship represents an observed structural connection only. It SHALL
NOT express exploitation chains, attack steps, or security interpretation; those
concerns are intentionally out of scope for this schema.

---

# Design Principles

An Asset Relationship SHALL be

- Canonical and reused verbatim across capabilities
- Directional and typed
- Evidence-backed through provenance
- Confidence-graded
- Traceable and auditable
- Implementation independent

---

# Identity

Every Asset Relationship SHALL contain

```yaml
relationship_id:

assessment_id:

schema_version:
```

`relationship_id` SHALL be unique within an assessment.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`schema_version` SHALL be `1.0.0`.

---

# Endpoints

Every Asset Relationship SHALL contain

```yaml
source_asset_id:

target_asset_id:
```

`source_asset_id` and `target_asset_id` SHALL reference existing
[Assets](asset.md) within the same assessment.

A relationship SHALL NOT reference an Asset outside its assessment.

---

# Type And Direction

Every Asset Relationship SHALL contain

```yaml
type:

directional:
```

`type` SHALL be one of

```
resolves-to

hosts

exposes

serves

redirects-to

belongs-to

member-of

trusts

references
```

`directional` SHALL be a boolean. When `true`, the relationship reads from
`source` to `target`. When `false`, the relationship is symmetric.

Additional relationship types MAY be introduced through the extension mechanism.

---

# Confidence

Every Asset Relationship SHALL contain

```yaml
confidence:
```

`confidence` SHALL be one of `Low`, `Medium`, `High`, or `Verified` and SHALL be
calculated according to [the confidence model](../skills/core/confidence-model.md).

Confidence measures certainty that the relationship is real and correctly typed.

---

# Provenance

Every Asset Relationship SHALL contain

```yaml
provenance:
```

`provenance` SHALL contain

```yaml
discovered_by:

discovered_at:

observations:

evidence:
```

`discovered_by` SHALL identify the capability that produced the relationship.

`observations` SHALL be an array of [observation](observation.md) references from
which the relationship was derived.

`evidence` SHALL be an array of [evidence](evidence.md) references corroborating
the relationship.

A relationship SHALL be traceable to at least one observation or evidence
reference.

---

# Attributes

An Asset Relationship MAY contain

```yaml
attributes:
```

`attributes` SHALL be a namespaced map of type-specific facts, such as the record
type for a `resolves-to` relationship or the status code for a `redirects-to`
relationship.

`attributes` SHALL contain observed facts only and SHALL NOT contain secrets.

---

# Extensions

An Asset Relationship MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata for new relationship types.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Asset Relationship object SHALL contain

- `relationship_id`
- `assessment_id`
- `schema_version`
- `source_asset_id`
- `target_asset_id`
- `type`
- `directional`
- `confidence`
- `provenance.discovered_by`
- `provenance.discovered_at`

---

# Validation Rules

A valid Asset Relationship object SHALL satisfy

- `source_asset_id` and `target_asset_id` reference existing Assets in the
  assessment
- `source_asset_id` and `target_asset_id` are not equal
- `type` is one of the allowed types or a declared extension type
- `directional` is a boolean
- `confidence` is one of the allowed confidence values
- `provenance` references at least one observation or evidence item
- The resulting asset graph contains no self-loops
- No secret material appears in `attributes` or `extensions`

---

# Relationships To Other Schemas

```
Assessment

└── Asset Graph

     ├── Assets (nodes)
     └── Asset Relationships (edges)

          ├── derived from Observations
          └── corroborated by Evidence
```

Asset Relationships are the edges of the canonical asset graph whose nodes are
[Assets](asset.md). They are derived from [observations](observation.md) and
corroborated by [evidence](evidence.md).

---

# Example Object

```yaml
relationship_id: assetrel-0031
assessment_id: asmt-42
schema_version: 1.0.0
source_asset_id: asset-0003
target_asset_id: asset-0007
type: exposes
directional: true
confidence: High
provenance:
  discovered_by: port-discovery
  discovered_at: 2026-07-25T18:41:00Z
  observations:
    - obs-1201
  evidence:
    - evidence-tcp-0007
attributes:
  port: 443
extensions: {}
```

---

# Extension Points

- New `type` values MAY be introduced for emerging structural relationships and
  declared in `extensions`.
- New `attributes` keys MAY be added per type without a schema change.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields or additional relationship types.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
