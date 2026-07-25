# Asset Schema

**File:** `schemas/asset.md`

**Version:** 1.0.0

---

# Purpose

The Asset Schema defines the canonical, implementation-independent representation
of an entity discovered or targeted during an assessment within the Robust
PenTest Platform (RPP).

An Asset is the canonical unit of the assessment attack surface. Every entity
that a Discovery capability identifies — a domain, host, service, port,
endpoint, web application, API, cloud resource, or identity — SHALL be
represented as an Asset.

Every Discovery and later domain capability SHALL produce Assets rather than
free-form objects. Assets are the shared vocabulary through which capabilities,
agents, and reports refer to the same real-world entity.

An Asset object represents an observed entity and its lifecycle metadata only.
It SHALL NOT contain security interpretation, findings, risk, or secrets.
Interpretation belongs to [findings](finding.md) and [risk](risk.md).

---

# Design Principles

An Asset SHALL be

- Canonical and reused verbatim across capabilities
- Deterministically identified
- Evidence-backed through provenance
- Scope-aware
- Confidence-graded
- Traceable and auditable
- Implementation independent

---

# Identity

Every Asset SHALL contain

```yaml
asset_id:

assessment_id:

schema_version:
```

`asset_id` SHALL be unique within an assessment.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`schema_version` SHALL be `1.0.0`.

---

# Classification

Every Asset SHALL contain

```yaml
type:

canonical_key:
```

`type` SHALL be one of

```
domain

subdomain

host

ip

service

port

endpoint

web-application

api

certificate

cloud-resource

identity

repository
```

`canonical_key` SHALL be the deterministic, normalized key that identifies the
entity within its `type`, such as a lowercased fully qualified domain name, an
`ip:port` pair, or a normalized URL. Equivalent entities SHALL produce equal
`canonical_key` values so that duplicate discovery converges on one Asset.

Additional types MAY be introduced through the extension mechanism.

---

# Value And Attributes

Every Asset SHALL contain

```yaml
value:
```

`value` SHALL be the human-readable representation of the entity, such as
`api.example.com` or `https://app.example.com/login`.

An Asset MAY contain

```yaml
attributes:
```

`attributes` SHALL be a namespaced map of type-specific facts, such as a
service banner, an HTTP title, a port protocol, or a cloud resource ARN.
`attributes` SHALL contain observed facts only and SHALL NOT contain security
interpretation or secrets.

---

# State

Every Asset SHALL contain

```yaml
state:
```

`state` SHALL be one of

```
suspected

confirmed

inactive
```

`suspected` SHALL denote an entity inferred but not yet corroborated.

`confirmed` SHALL denote an entity corroborated by direct observation.

`inactive` SHALL denote an entity that no longer responds or has been
decommissioned during the assessment.

---

# Confidence

Every Asset SHALL contain

```yaml
confidence:
```

`confidence` SHALL be one of `Low`, `Medium`, `High`, or `Verified` and SHALL be
calculated according to [the confidence model](../skills/core/confidence-model.md).

Confidence measures certainty that the Asset is real and correctly classified.
Confidence SHALL NOT represent severity or risk.

---

# Scope Status

Every Asset SHALL contain

```yaml
scope_status:
```

`scope_status` SHALL be one of

```
in_scope

out_of_scope

unknown
```

`scope_status` SHALL be determined by evaluating the Asset against the assessment
[scope](scope.md). An Asset that is `out_of_scope` SHALL NOT be acted upon by any
intrusive capability, as enforced by the
[Policy Engine](../skills/shared/policy-engine/README.md).

---

# Provenance

Every Asset SHALL contain

```yaml
provenance:
```

`provenance` SHALL contain

```yaml
discovered_by:

discovered_at:

method:

observations:

evidence:
```

`discovered_by` SHALL identify the capability that produced the Asset.

`method` SHALL describe how the Asset was discovered, such as `dns-enumeration`
or `passive-observation`.

`observations` SHALL be an array of [observation](observation.md) references from
which the Asset was derived.

`evidence` SHALL be an array of [evidence](evidence.md) references corroborating
the Asset.

An Asset SHALL be traceable to at least one observation or evidence reference.

---

# Relationships

Every Asset MAY contain

```yaml
relationships:
```

`relationships` SHALL be an array of [asset relationship](asset-relationship.md)
references describing typed edges to other Assets, such as a subdomain that
`resolves-to` a host, or a host that `exposes` a service.

Relationships SHALL be expressed through the canonical
[Asset Relationship schema](asset-relationship.md) rather than embedded ad hoc.

---

# Extensions

An Asset MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata for new asset types or attributes.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Asset object SHALL contain

- `asset_id`
- `assessment_id`
- `schema_version`
- `type`
- `canonical_key`
- `value`
- `state`
- `confidence`
- `scope_status`
- `provenance.discovered_by`
- `provenance.discovered_at`

---

# Validation Rules

A valid Asset object SHALL satisfy

- `type` is one of the allowed types or a declared extension type
- `canonical_key` is deterministic; equivalent entities share a key
- `state` is one of the allowed states
- `confidence` is one of the allowed confidence values
- `scope_status` is one of the allowed values
- `provenance` references at least one observation or evidence item
- `relationships` reference existing Assets within the assessment
- No secret material appears in `attributes` or `extensions`

---

# Relationships To Other Schemas

```
Assessment

└── Assets

     ├── derived from Observations
     ├── corroborated by Evidence
     ├── connected by Asset Relationships
     ├── evaluated against Scope (scope_status)
     └── referenced by Findings and Risk
```

An Asset belongs to exactly one [assessment](assessment.md). It is derived from
[observations](observation.md), corroborated by [evidence](evidence.md),
connected to other Assets through [asset relationships](asset-relationship.md),
evaluated against [scope](scope.md), and referenced by
[findings](finding.md) and [risk](risk.md).

---

# Example Object

```yaml
asset_id: asset-0007
assessment_id: asmt-42
schema_version: 1.0.0
type: service
canonical_key: 93.184.216.34:443
value: https-service on 93.184.216.34:443
attributes:
  protocol: https
  server: nginx
  http_title: Example App
state: confirmed
confidence: High
scope_status: in_scope
provenance:
  discovered_by: port-discovery
  discovered_at: 2026-07-25T18:40:00Z
  method: port-scan
  observations:
    - obs-1201
  evidence:
    - evidence-tcp-0007
relationships:
  - assetrel-0031
extensions: {}
```

---

# Extension Points

- New `type` values MAY be introduced for emerging asset classes and declared in
  `extensions`.
- New `attributes` keys MAY be added per type without a schema change.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields or additional asset types.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
