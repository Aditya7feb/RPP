# HTTP Transaction Schema

**File:** `schemas/http-transaction.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Transaction Schema defines the canonical representation of one complete
HTTP exchange executed by the HTTP Client Shared Skill.

A transaction links an [HTTP Request](http-request.md), its final
[HTTP Response](http-response.md), any intervening
[HTTP Redirect](http-redirect.md) chain, [HTTP Timing](http-timing.md), and the
[TLS Connection](tls-connection.md) used. It is the primary unit exported by the
`ExportTransaction` operation defined in
[the HTTP Client interface](../skills/shared/http-client/interface.md).

The HTTP Transaction object represents observed activity only. It SHALL NOT
contain security interpretation or finding.

---

# Design Principles

An HTTP Transaction SHALL be

- Traceable
- Lifecycle aware
- Evidence backed
- Adapter independent
- Assessment scoped
- Reproducible
- Explicit about outcome

---

# Identity

Every HTTP Transaction SHALL contain

```yaml
transaction_id:

schema_version:
```

`transaction_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every HTTP Transaction SHALL contain

```yaml
assessment_id:

task_id:

skill_id:
```

`assessment_id` identifies the owning assessment.

`task_id` identifies the task that authorized the transaction.

`skill_id` identifies the domain skill that initiated the transaction.

---

# Session Relationship

An HTTP Transaction MAY contain

```yaml
session_id:
```

`session_id` SHALL reference the [HTTP Session](http-session.md) that owns the
transaction when executed within a session.

---

# Request and Response

Every HTTP Transaction SHALL contain

```yaml
request_id:

response_id:
```

`request_id` SHALL reference the [HTTP Request](http-request.md).

`response_id` SHALL reference the final [HTTP Response](http-response.md).

`response_id` MAY be absent when `outcome` is `failed` before any response was
received.

---

# Redirect Chain

An HTTP Transaction MAY contain

```yaml
redirect_id:
```

`redirect_id` SHALL reference the [HTTP Redirect](http-redirect.md) chain when
one or more redirects occurred.

---

# Timing

Every HTTP Transaction SHALL contain

```yaml
timing_id:
```

`timing_id` SHALL reference the [HTTP Timing](http-timing.md) object for the
transaction.

---

# TLS Connection

An HTTP Transaction MAY contain

```yaml
tls_connection_id:
```

`tls_connection_id` SHALL reference the [TLS Connection](tls-connection.md) when
the transaction used HTTPS.

---

# Transport Metadata

Every HTTP Transaction SHALL contain

```yaml
adapter:

http_version:
```

`adapter` SHALL identify the transport adapter that executed the transaction.

`http_version` SHALL be one of

```
HTTP/1.1

HTTP/2

HTTP/3
```

Transport-specific objects SHALL NOT be exposed.

---

# Lifecycle State

Every HTTP Transaction SHALL contain

```yaml
started_at:

completed_at:

outcome:
```

`started_at` SHALL be an RFC 3339 UTC timestamp.

`completed_at` SHALL be an RFC 3339 UTC timestamp on or after `started_at`.

`outcome` SHALL be one of

```
completed

failed

cancelled

timed_out
```

---

# Error Reference

An HTTP Transaction MAY contain

```yaml
error:
```

`error` SHALL be present when `outcome` is `failed`, `cancelled`, or
`timed_out`.

`error` SHALL conform to the canonical error structure defined in
[the HTTP Client error model](../skills/shared/http-client/error-model.md).

---

# Metrics

An HTTP Transaction MAY contain

```yaml
metrics:
```

`metrics` MAY include

```yaml
request_size:

response_size:

retry_count:

redirect_count:

duration:
```

Metrics SHALL support observability and SHALL NOT alter transaction identity.

---

# Evidence

Every HTTP Transaction SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Transaction MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
transaction_id: httptxn-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
task_id: task-042
skill_id: recon.http
session_id: httpsession-01
request_id: httpreq-01
response_id: httpresp-01
redirect_id: httpredirect-01
timing_id: httptiming-01
tls_connection_id: tlsconn-01
adapter: httpx
http_version: HTTP/2
started_at: '2026-07-25T10:00:00Z'
completed_at: '2026-07-25T10:00:01Z'
outcome: completed
metrics:
  request_size: 128
  response_size: 4096
  retry_count: 0
  redirect_count: 2
  duration: 1.02s
evidence:
  - evidence-http-05
```

---

# Validation Rules

A valid HTTP Transaction object SHALL contain

- Transaction ID
- Schema Version
- Assessment ID
- Task ID
- Skill ID
- Request ID
- Timing Reference
- Adapter
- HTTP Version
- Started Timestamp
- Completed Timestamp
- Outcome
- Evidence References

A valid HTTP Transaction object SHALL satisfy

- `outcome` is one of the allowed values
- `response_id` is present when `outcome` is `completed`
- `error` is present when `outcome` is `failed`, `cancelled`, or `timed_out`
- `tls_connection_id` is present when the request scheme is HTTPS
- No secret material appears in `extensions`

---

# Relationships

```
HTTP Transaction

├── HTTP Request
├── HTTP Response
├── HTTP Redirect
├── HTTP Timing
├── HTTP Session
├── TLS Connection
└── Evidence
```

---

# Versioning

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Extension Points

Future versions MAY introduce

- Multiplexed stream metadata
- Server push transactions
- Distributed trace identifiers
- Adapter health scoring

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Transaction object provides a complete, traceable record of one
HTTP exchange from request through final response.

It enables platform components to correlate requests, responses, redirects,
timing, TLS context, and evidence for reporting and audit.
