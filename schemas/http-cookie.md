# HTTP Cookie Schema

**File:** `schemas/http-cookie.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Cookie Schema defines the canonical representation of a single HTTP
cookie managed by the HTTP Client Shared Skill.

Cookies are parsed from `Set-Cookie` response headers and applied to subsequent
requests. This schema represents one cookie and its attributes as defined by
RFC 6265.

The HTTP Cookie object represents state only. It SHALL NOT contain security
interpretation or finding.

---

# Design Principles

An HTTP Cookie SHALL be

- Faithful to RFC 6265
- Session scoped
- Attribute complete
- Expiry aware
- Safe to reference
- Redacted where sensitive

---

# Identity

Every HTTP Cookie SHALL contain

```yaml
cookie_id:

schema_version:
```

`cookie_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Session Relationship

Every HTTP Cookie SHALL contain

```yaml
session_id:

assessment_id:
```

`session_id` SHALL reference the owning [HTTP Session](http-session.md).

`assessment_id` identifies the owning assessment.

Cookies SHALL remain scoped to their session unless explicitly shared.

---

# Core Fields

Every HTTP Cookie SHALL contain

```yaml
name:

value:
```

`name` SHALL be the cookie name.

`value` SHALL be the cookie value as a string.

`value` SHALL be redacted in exported evidence when `sensitive` is `true`.

---

# Scope Attributes

An HTTP Cookie MAY contain

```yaml
domain:

path:
```

`domain` SHALL describe the host scope of the cookie.

`path` SHALL describe the URL path scope of the cookie.

When absent, scope SHALL default to the origin that issued the cookie.

---

# Expiry Attributes

An HTTP Cookie MAY contain

```yaml
expires:

max_age:

persistent:
```

`expires` SHALL be an RFC 3339 UTC timestamp when present.

`max_age` SHALL be an integer number of seconds when present.

`persistent` SHALL be a boolean. A cookie SHALL be persistent when `expires` or
`max_age` is present, and a session cookie otherwise.

---

# Security Attributes

An HTTP Cookie MAY contain

```yaml
secure:

http_only:

same_site:
```

`secure` SHALL be a boolean indicating the `Secure` attribute.

`http_only` SHALL be a boolean indicating the `HttpOnly` attribute.

`same_site` SHALL be one of

```
Strict

Lax

None
```

When `same_site` is `None`, `secure` SHOULD be `true`.

These attributes are recorded faithfully as observed. Interpreting them as
weaknesses SHALL remain the responsibility of domain skills, not this schema.

---

# Source

An HTTP Cookie MAY contain

```yaml
source_response_id:

set_cookie_order:
```

`source_response_id` SHALL reference the [HTTP Response](http-response.md) whose
`Set-Cookie` header produced the cookie.

`set_cookie_order` SHALL be a zero-based integer when multiple `Set-Cookie`
headers are present.

---

# Sensitivity

An HTTP Cookie MAY contain

```yaml
sensitive:
```

`sensitive` SHALL be a boolean indicating that the cookie carries session or
authentication material.

When `sensitive` is `true`, `value` SHALL be redacted in exported evidence.

---

# Evidence

An HTTP Cookie MAY contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

---

# Example

```yaml
cookie_id: httpcookie-01
schema_version: 1.0.0
session_id: httpsession-01
assessment_id: assessment-2026-001
name: SESSIONID
value: '[REDACTED]'
domain: example.com
path: /
expires: '2026-07-25T12:00:00Z'
persistent: true
secure: true
http_only: true
same_site: Lax
source_response_id: httpresp-01
set_cookie_order: 0
sensitive: true
evidence:
  - evidence-http-03
```

---

# Validation Rules

A valid HTTP Cookie object SHALL contain

- Cookie ID
- Schema Version
- Session ID
- Assessment ID
- Name
- Value

A valid HTTP Cookie object SHALL satisfy

- `same_site`, when present, is `Strict`, `Lax`, or `None`
- `persistent` is `true` when `expires` or `max_age` is present
- `value` is redacted when `sensitive` is `true` in exported evidence

---

# Relationships

```
HTTP Cookie

├── HTTP Session
├── HTTP Response
└── Evidence
```

Cookies are applied to [HTTP Request](http-request.md) objects and parsed from
[HTTP Response](http-response.md) objects.

---

# Versioning

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Extension Points

Future versions MAY introduce

- Cookie prefixes such as `__Host-` and `__Secure-`
- Partitioned cookie metadata
- Priority attributes

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Cookie object provides a faithful, RFC 6265 aligned
representation of one cookie and its attributes.

It enables consistent cookie persistence and reuse across requests while
protecting sensitive values.
