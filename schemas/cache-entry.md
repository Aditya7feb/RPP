# Cache Entry Schema

**File:** `schemas/cache-entry.md`

**Version:** 1.0.0

---

# Purpose

The Cache Entry Schema defines the canonical, implementation-independent
representation of a cached value within the Robust PenTest Platform (RPP).

A cache entry describes a single stored result: its key, value reference,
freshness metadata, validators, and provenance. It is consumed by the
[Cache](../skills/shared/cache/README.md) shared package and referenced by
packages that reuse expensive or repeated results, including the
[DNS Client](../skills/shared/dns-client/README.md),
[TLS Client](../skills/shared/tls-client/README.md), and
[HTTP Client](../skills/shared/http-client/README.md).

A Cache Entry object represents stored data and its lifecycle metadata only. It
SHALL NOT contain security interpretation, findings, or embedded secrets.

---

# Design Principles

A Cache Entry SHALL be

- Deterministic in identity
- Freshness aware
- Provenance bearing
- Transport independent
- Reusable across packages
- Safe to reference

---

# Identity

Every Cache Entry SHALL contain

```yaml
entry_id:

schema_version:

key:
```

`entry_id` SHALL be unique within a cache namespace.

`schema_version` SHALL be `1.0.0`.

`key` SHALL be the canonical, deterministic key under which the value is stored.

---

# Key Composition

Every Cache Entry SHALL contain

```yaml
key_components:
```

`key_components` SHALL contain

```yaml
namespace:

operation:

parameters_digest:
```

`namespace` SHALL identify the logical cache, such as `dns` or `http`.

`operation` SHALL identify the operation whose result is cached, such as
`resolve` or `get`.

`parameters_digest` SHALL be a deterministic digest of the normalized operation
parameters. Equivalent operations SHALL produce equal digests.

`key_components` SHALL NOT contain secret material.

---

# Value

Every Cache Entry SHALL contain

```yaml
value:
```

`value` SHALL contain

```yaml
content_type:

content_ref:

size_bytes:
```

`content_type` SHALL describe the canonical type of the cached value.

`content_ref` SHALL reference the stored value. Large values SHOULD be stored by
reference rather than inline.

`size_bytes` SHALL be a non-negative integer.

A Cache Entry MAY store small values inline.

```yaml
inline_value:
```

`inline_value` SHALL be present only when `content_ref` is absent.

---

# Freshness

Every Cache Entry SHALL contain

```yaml
freshness:
```

`freshness` SHALL contain

```yaml
created_at:

expires_at:

ttl:
```

`created_at` SHALL be the time the entry was stored.

`expires_at` SHALL be the absolute time after which the entry is stale.

`ttl` SHALL be the duration used to compute `expires_at`.

A Cache Entry MAY contain

```yaml
stale_while_revalidate:
```

`stale_while_revalidate` SHALL be a duration during which a stale entry MAY be
served while a fresh value is obtained.

---

# Validators

A Cache Entry MAY contain

```yaml
validators:
```

`validators` SHALL contain

```yaml
etag:

last_modified:

version:
```

Validators support conditional revalidation without transferring the full
value. Their interpretation is the responsibility of the consuming package.

---

# Provenance

Every Cache Entry SHALL contain

```yaml
provenance:
```

`provenance` SHALL contain

```yaml
assessment_id:

produced_by:

source_operation:
```

`produced_by` SHALL identify the package that produced the value.

`source_operation` SHALL identify the originating operation for auditing.

Provenance supports evidence correlation and cache auditing.

---

# Scope

Every Cache Entry SHALL contain

```yaml
scope:
```

`scope` SHALL be one of

```
assessment

session

global
```

`scope` bounds the visibility and reuse of the entry. An entry SHALL NOT be
served outside its scope.

---

# Extensions

A Cache Entry MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Cache Entry object SHALL contain

- `entry_id`
- `schema_version`
- `key`
- `key_components.namespace`
- `key_components.operation`
- `key_components.parameters_digest`
- `value.content_type`
- `value.size_bytes`
- `freshness.created_at`
- `freshness.expires_at`
- `freshness.ttl`
- `provenance.assessment_id`
- `provenance.produced_by`
- `scope`

---

# Validation Rules

A valid Cache Entry object SHALL satisfy

- `key` is deterministic given `key_components`
- Exactly one of `value.content_ref` or `inline_value` is present
- `value.size_bytes` is a non-negative integer
- `freshness.expires_at` is greater than or equal to `freshness.created_at`
- `stale_while_revalidate`, when present, is a non-negative duration
- `scope` is one of the allowed scopes
- No secret material appears in any field, including `extensions`

---

# Relationships

```
Cache Entry

├── produced by a shared package operation
├── stored and retrieved by the Cache shared package
├── keyed by deterministic key_components
├── bounded by scope
└── correlated to evidence through provenance
```

A Cache Entry is produced when a package stores the result of an operation. The
[Cache](../skills/shared/cache/README.md) shared package stores and retrieves
entries by key. Provenance correlates entries with
[evidence](evidence.md).

---

# Example Object

```yaml
entry_id: cache-dns-0001
schema_version: 1.0.0
key: dns:resolve:9f2c1a...
key_components:
  namespace: dns
  operation: resolve
  parameters_digest: 9f2c1a...
value:
  content_type: dns-response
  content_ref: artifact://dns/9f2c1a
  size_bytes: 512
freshness:
  created_at: 2026-07-25T11:30:00Z
  expires_at: 2026-07-25T11:35:00Z
  ttl: 300s
  stale_while_revalidate: 60s
validators:
  version: "1"
provenance:
  assessment_id: asmt-42
  produced_by: dns-client
  source_operation: resolve-a-record
scope: assessment
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional validators or
freshness controls.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
