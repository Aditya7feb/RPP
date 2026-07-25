# HTTP Request Schema

**File:** `schemas/http-request.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Request Schema defines the canonical representation of a single HTTP
request issued by the HTTP Client Shared Skill.

The schema describes the request independently of any transport implementation.
It SHALL be produced by the `BuildRequest` operation and consumed by the
`SendRequest`, `SendBatch`, `Download`, and `Upload` operations defined in
[the HTTP Client interface](../skills/shared/http-client/interface.md).

The HTTP Request object represents intent only. It SHALL NOT contain any
response data, security interpretation, or finding.

---

# Design Principles

An HTTP Request SHALL be

- Transport independent
- Deterministic
- Assessment scoped
- Evidence backed
- Explicit about its body encoding
- Safe to reference
- Free of embedded secrets

---

# Identity

Every HTTP Request SHALL contain

```yaml
request_id:

schema_version:
```

`request_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every HTTP Request SHALL contain

```yaml
assessment_id:

task_id:

skill_id:
```

`assessment_id` identifies the owning assessment.

`task_id` identifies the task that authorized the request.

`skill_id` identifies the domain skill that constructed the request.

---

# Session Relationship

An HTTP Request MAY contain

```yaml
session_id:
```

`session_id` SHALL reference an [HTTP Session](http-session.md) when the request
executes within a session context.

When `session_id` is absent the request SHALL be treated as sessionless.

---

# Target

Every HTTP Request SHALL contain

```yaml
method:

url:

http_version:
```

`method` SHALL be one of

```
GET

POST

PUT

PATCH

DELETE

OPTIONS

HEAD

TRACE

CONNECT
```

`url` SHALL be an absolute URL including scheme and host.

`http_version` SHALL be one of

```
HTTP/1.1

HTTP/2

HTTP/3
```

`HTTP/3` SHALL require an explicitly enabled adapter.

---

# Query Parameters

An HTTP Request MAY contain

```yaml
query:
```

`query` SHALL be an ordered array of name and value pairs.

Query parameters SHALL be represented independently from `url`.

Example

```yaml
query:
  - name: page
    value: '1'
  - name: limit
    value: '25'
```

---

# Headers

An HTTP Request MAY contain

```yaml
headers:
```

`headers` SHALL be an array of [HTTP Header](http-header.md) objects.

Header ordering SHOULD be preserved for evidence fidelity.

---

# Cookies

An HTTP Request MAY contain

```yaml
cookies:
```

`cookies` SHALL be an array of [HTTP Cookie](http-cookie.md) references or
objects applied to the request.

Cookie management SHALL remain the responsibility of the HTTP Client.

---

# Body

An HTTP Request MAY contain

```yaml
body:
```

When present, `body` SHALL contain

```yaml
type:

encoding:

content_reference:

size:
```

`type` SHALL be one of

```
json

xml

html

text

binary

multipart

form_urlencoded
```

`encoding` SHALL describe the character or transfer encoding when applicable.

`content_reference` SHALL reference stored content rather than embedding large
payloads inline.

`size` SHALL be the body size in bytes.

A `body` SHALL NOT be present when `method` is `GET`, `HEAD`, or `TRACE`.

---

# Authentication Reference

An HTTP Request MAY contain

```yaml
authentication_profile:
```

`authentication_profile` SHALL reference a shared
[Authentication](../skills/shared/authentication/README.md) profile.

Credentials SHALL NEVER be embedded directly in the request object.

---

# Execution Options

An HTTP Request MAY contain

```yaml
options:
```

`options` MAY include

```yaml
follow_redirects:

verify_tls:

timeout:

proxy_profile:

compression:

stream:

retry_policy:
```

Options SHALL influence execution without altering request identity.

---

# Evidence

Every HTTP Request SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Request MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
request_id: httpreq-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
task_id: task-042
skill_id: recon.http
session_id: httpsession-01
method: POST
url: https://api.example.com/graphql
http_version: HTTP/2
query:
  - name: trace
    value: 'true'
headers:
  - name: Content-Type
    value: application/json
  - name: Accept
    value: application/json
cookies:
  - httpcookie-01
body:
  type: json
  encoding: utf-8
  content_reference: content-store/httpreq-01-body
  size: 128
authentication_profile: api-service-account
options:
  follow_redirects: false
  verify_tls: true
  timeout: 30s
evidence:
  - evidence-http-01
```

---

# Validation Rules

A valid HTTP Request object SHALL contain

- Request ID
- Schema Version
- Assessment ID
- Task ID
- Skill ID
- Method
- URL
- HTTP Version
- Evidence References

A valid HTTP Request object SHALL satisfy

- `method` is a supported method
- `url` is absolute
- `body` is absent for `GET`, `HEAD`, and `TRACE`
- No secret material appears in `headers`, `cookies`, or `extensions`

---

# Relationships

```
HTTP Request

├── HTTP Header
├── HTTP Cookie
├── HTTP Session
├── Authentication Profile
└── Evidence
```

An HTTP Request is paired with an [HTTP Response](http-response.md) inside an
[HTTP Transaction](http-transaction.md).

---

# Versioning

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Extension Points

Future versions MAY introduce

- Trailer headers
- Early hints
- Priority signaling
- Protocol-specific frame metadata

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Request object provides a complete, transport-independent
description of one outbound HTTP request.

It enables the HTTP Client to execute the request through any adapter while
preserving evidence, assessment context, and reproducibility.
