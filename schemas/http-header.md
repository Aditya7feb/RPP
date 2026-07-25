# HTTP Header Schema

**File:** `schemas/http-header.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Header Schema defines the canonical representation of a single HTTP
header field as observed or constructed by the HTTP Client Shared Skill.

Headers appear on both [HTTP Request](http-request.md) and
[HTTP Response](http-response.md) objects. This schema provides one consistent
representation for both directions.

The HTTP Header object represents a name and value pair only. It SHALL NOT
contain security interpretation or finding.

---

# Design Principles

An HTTP Header SHALL be

- Faithful to the wire representation
- Order preserving
- Case aware
- Duplicate aware
- Direction aware
- Safe to reference

---

# Identity

Every HTTP Header SHALL contain

```yaml
name:

value:
```

`name` SHALL be the header field name exactly as transmitted or constructed.

`value` SHALL be the header field value as a string.

---

# Normalization

An HTTP Header MAY contain

```yaml
normalized_name:
```

`normalized_name` SHALL be the lowercase form of `name`.

HTTP header names are case insensitive. Consumers SHOULD match on
`normalized_name` while preserving `name` for evidence fidelity.

---

# Direction

An HTTP Header MAY contain

```yaml
direction:
```

`direction` SHALL be one of

```
request

response
```

`direction` SHOULD be present when a header is stored independently of its
parent object.

---

# Ordering

An HTTP Header MAY contain

```yaml
order:
```

`order` SHALL be a zero-based integer describing the header position in the
original sequence.

`order` SHOULD be preserved when duplicate header names occur.

---

# Multi-Value Headers

An HTTP Header MAY contain

```yaml
values:
```

`values` SHALL be an array of strings when a single header name carries
multiple comma-separated or repeated values.

When `values` is present, `value` SHALL contain the concatenated raw value for
fidelity.

---

# Sensitivity

An HTTP Header MAY contain

```yaml
sensitive:
```

`sensitive` SHALL be a boolean indicating that the header value carries
credentials or secrets.

Headers such as `Authorization`, `Cookie`, `Set-Cookie`, and `Proxy-Authorization`
SHOULD be marked `sensitive`.

When `sensitive` is `true`, `value` SHALL be redacted in exported evidence.

---

# Example

```yaml
name: Content-Type
normalized_name: content-type
value: application/json
direction: response
order: 3
sensitive: false
```

Sensitive header example

```yaml
name: Authorization
normalized_name: authorization
value: '[REDACTED]'
direction: request
order: 0
sensitive: true
```

---

# Validation Rules

A valid HTTP Header object SHALL contain

- Name
- Value

A valid HTTP Header object SHALL satisfy

- `name` is a non-empty string
- `normalized_name`, when present, is the lowercase form of `name`
- `direction`, when present, is `request` or `response`
- `value` is redacted when `sensitive` is `true` in exported evidence

---

# Relationships

```
HTTP Header

├── HTTP Request
└── HTTP Response
```

An HTTP Header is always owned by an HTTP Request or an HTTP Response.

---

# Versioning

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Extension Points

Future versions MAY introduce

- Structured field parsing per RFC 8941
- Header provenance metadata
- Protocol-specific pseudo-header handling

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Header object provides a faithful, direction-aware
representation of one HTTP header field.

It enables consistent header handling across requests, responses, and evidence
while protecting sensitive values.
