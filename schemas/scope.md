# Scope Schema

**File:** `schemas/scope.md`

**Version:** 1.0.0

---

# Purpose

The Scope Schema defines the canonical, implementation-independent representation
of the assessment scope within the Robust PenTest Platform (RPP).

Scope declares **what may be tested**. It is the authoritative definition of the
targets that are inside or outside the boundary of an assessment. Scope is
defined independently from the [Rules of Engagement](rules-of-engagement.md),
which declare **what actions are permitted** against in-scope targets.

Scope is evaluated to determine the `scope_status` of every [Asset](asset.md) and
is consulted by the [Policy Engine](../skills/shared/policy-engine/README.md)
before any capability acts against a target.

A Scope object represents boundary configuration only. It SHALL NOT contain
findings, risk, or secrets.

---

# Design Principles

A Scope SHALL be

- Declarative
- Deterministic in matching
- Authoritative for target inclusion
- Independent from Rules of Engagement
- Auditable
- Implementation independent

---

# Identity

Every Scope SHALL contain

```yaml
scope_id:

assessment_id:

schema_version:
```

`scope_id` SHALL be unique within a configuration namespace.

`assessment_id` SHALL reference the owning [assessment](assessment.md).

`schema_version` SHALL be `1.0.0`.

---

# Inclusions

Every Scope SHALL contain

```yaml
include:
```

`include` SHALL contain

```yaml
domains:

subdomains:

hosts:

ip_ranges:

applications:

api_endpoints:

cloud_accounts:
```

Each field SHALL be an array of matchers. A target is in scope when it matches at
least one `include` matcher and no `exclude` matcher.

`ip_ranges` SHALL be expressed as address ranges such as CIDR blocks.

Matchers MAY use wildcard patterns for domains and paths.

---

# Exclusions

Every Scope SHALL contain

```yaml
exclude:
```

`exclude` SHALL contain the same fields as `include`.

Exclusions SHALL take precedence over inclusions. A target matching any
`exclude` matcher SHALL be out of scope regardless of `include` matchers.

`exclude` SHALL also implicitly cover loopback and link-local ranges unless a
matcher explicitly includes them.

---

# Matching Rules

Every Scope SHALL contain

```yaml
matching:
```

`matching` SHALL contain

```yaml
case_sensitive:

wildcard_domains:

subdomain_inheritance:
```

`case_sensitive` SHALL be a boolean; host and domain matching SHOULD be
case-insensitive.

`wildcard_domains` SHALL be a boolean enabling `*.example.com` style matchers.

`subdomain_inheritance` SHALL be a boolean. When `true`, including a domain
includes its subdomains unless explicitly excluded.

Matching SHALL be deterministic: the same target and Scope SHALL always yield the
same result.

---

# Default Disposition

Every Scope SHALL contain

```yaml
default_disposition:
```

`default_disposition` SHALL be one of `out_of_scope` or `unknown` and SHALL apply
to targets matching neither `include` nor `exclude`.

`default_disposition` SHALL NOT be `in_scope`; membership SHALL be explicit.

---

# Extensions

A Scope MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Scope object SHALL contain

- `scope_id`
- `assessment_id`
- `schema_version`
- `include`
- `exclude`
- `matching`
- `default_disposition`

---

# Validation Rules

A valid Scope object SHALL satisfy

- At least one `include` matcher is defined
- `exclude` takes precedence over `include`
- `ip_ranges` are valid address ranges
- `default_disposition` is `out_of_scope` or `unknown`, never `in_scope`
- Matching is deterministic and case handling is explicit
- No secret material appears in `extensions`

---

# Relationships To Other Schemas

```
Assessment

├── Scope (what may be tested)
│     ├── evaluated to set Asset.scope_status
│     └── consulted by the Policy Engine
│
└── Rules of Engagement (what actions are permitted)
```

Scope belongs to exactly one [assessment](assessment.md). It is evaluated to set
the `scope_status` of each [Asset](asset.md) and is consulted, together with the
[Rules of Engagement](rules-of-engagement.md), by the
[Policy Engine](../skills/shared/policy-engine/README.md).

---

# Example Object

```yaml
scope_id: scope-asmt-42
assessment_id: asmt-42
schema_version: 1.0.0
include:
  domains:
    - example.com
  subdomains: []
  hosts: []
  ip_ranges:
    - 93.184.216.0/24
  applications:
    - https://app.example.com
  api_endpoints:
    - https://api.example.com
  cloud_accounts: []
exclude:
  domains:
    - status.example.com
  ip_ranges:
    - 93.184.216.1/32
matching:
  case_sensitive: false
  wildcard_domains: true
  subdomain_inheritance: true
default_disposition: out_of_scope
extensions: {}
```

---

# Extension Points

- New matcher categories MAY be introduced for emerging target classes.
- Consumers SHALL ignore unknown optional fields for forward compatibility.

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional matcher categories.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
