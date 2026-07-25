# HTTP Response Schema

**File:** `schemas/http-response.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Response Schema defines the canonical representation of a single HTTP
response received by the HTTP Client Shared Skill.

The schema describes the normalized response independently of any transport
implementation. It SHALL be produced when an [HTTP Request](http-request.md)
completes and SHALL be paired with that request inside an
[HTTP Transaction](http-transaction.md).

The HTTP Response object represents observed data only. It SHALL NOT contain
security interpretation, technology fingerprint, or finding.

---

# Design Principles

An HTTP Response SHALL be

- Transport independent
- Faithful to observed data
- Assessment scoped
- Evidence backed
- Explicit about decoding
- Safe to reference
- Free of embedded secrets

---

# Identity

Every HTTP Response SHALL contain

```yaml
response_id:

schema_version:
```

`response_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Request Relationship

Every HTTP Response SHALL contain

```yaml
request_id:

assessment_id:

task_id:
```

`request_id` SHALL reference the originating [HTTP Request](http-request.md).

`assessment_id` identifies the owning assessment.

`task_id` identifies the task that authorized the request.

---

# Status

Every HTTP Response SHALL contain

```yaml
status_code:

reason_phrase:

http_version:
```

`status_code` SHALL be an integer from 100 through 599.

`reason_phrase` SHALL be the textual status when provided by the transport.

`http_version` SHALL be one of

```
HTTP/1.1

HTTP/2

HTTP/3
```

---

# Headers

Every HTTP Response SHALL contain

```yaml
headers:
```

`headers` SHALL be an array of [HTTP Header](http-header.md) objects.

Header ordering and duplicates SHOULD be preserved for evidence fidelity.

---

# Cookies

An HTTP Response MAY contain

```yaml
cookies:
```

`cookies` SHALL be an array of [HTTP Cookie](http-cookie.md) objects parsed
from `Set-Cookie` headers.

Cookie persistence SHALL remain the responsibility of the HTTP Client.

---

# Body

An HTTP Response MAY contain

```yaml
body:
```

When present, `body` SHALL contain

```yaml
mime_type:

charset:

content_reference:

size:

truncated:
```

`mime_type` SHALL be the resolved MIME type of the response body.

`charset` SHALL describe the character encoding when applicable.

`content_reference` SHALL reference stored content rather than embedding large
payloads inline.

`size` SHALL be the decoded body size in bytes.

`truncated` SHALL be a boolean indicating whether the body was truncated by
`maximum_response_size`.

---

# Content Encoding

An HTTP Response MAY contain

```yaml
content_encoding:

decoded:
```

`content_encoding` SHALL record the original transfer encoding.

Supported values MAY include

```
gzip

deflate

br

identity
```

`decoded` SHALL be a boolean indicating whether the body was decompressed.

---

# Transfer Metadata

An HTTP Response MAY contain

```yaml
content_length:

chunked:
```

`content_length` SHALL be the declared content length when present.

`chunked` SHALL be a boolean indicating chunked transfer encoding.

---

# Redirect Relationship

An HTTP Response MAY contain

```yaml
redirect_id:

final:
```

`redirect_id` SHALL reference an [HTTP Redirect](http-redirect.md) chain when
one or more redirects occurred.

`final` SHALL be a boolean indicating whether this response is the terminal
response of a redirect chain.

---

# TLS Relationship

An HTTP Response MAY contain

```yaml
tls_connection_id:
```

`tls_connection_id` SHALL reference a
[TLS Connection](tls-connection.md) when the request used HTTPS.

TLS metadata SHALL NOT be duplicated inside the response object.

---

# Timing Relationship

Every HTTP Response SHALL contain

```yaml
timing_id:
```

`timing_id` SHALL reference an [HTTP Timing](http-timing.md) object.

---

# Evidence

Every HTTP Response SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Response MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
response_id: httpresp-01
schema_version: 1.0.0
request_id: httpreq-01
assessment_id: assessment-2026-001
task_id: task-042
status_code: 200
reason_phrase: OK
http_version: HTTP/2
headers:
  - name: content-type
    value: application/json
  - name: content-encoding
    value: gzip
cookies:
  - httpcookie-02
body:
  mime_type: application/json
  charset: utf-8
  content_reference: content-store/httpresp-01-body
  size: 4096
  truncated: false
content_encoding: gzip
decoded: true
content_length: 1200
chunked: false
final: true
tls_connection_id: tlsconn-01
timing_id: httptiming-01
evidence:
  - evidence-http-02
```

---

# Validation Rules

A valid HTTP Response object SHALL contain

- Response ID
- Schema Version
- Request ID
- Assessment ID
- Task ID
- Status Code
- HTTP Version
- Headers
- Timing Reference
- Evidence References

A valid HTTP Response object SHALL satisfy

- `status_code` is between 100 and 599
- `tls_connection_id` is present when the request scheme is HTTPS
- `redirect_id` is present when `final` follows one or more redirects
- No secret material appears in `headers`, `cookies`, or `extensions`

---

# Relationships

```
HTTP Response

├── HTTP Request
├── HTTP Header
├── HTTP Cookie
├── HTTP Redirect
├── HTTP Timing
├── TLS Connection
└── Evidence
```

An HTTP Response is paired with an [HTTP Request](http-request.md) inside an
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
- Server push metadata
- Early hints
- Protocol-specific frame metadata

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Response object provides a complete, transport-independent
record of one received HTTP response.

It enables domain skills to interpret responses consistently while preserving
evidence, timing, and TLS context across every adapter.
