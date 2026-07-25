# HTTP Redirect Schema

**File:** `schemas/http-redirect.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Redirect Schema defines the canonical representation of a redirect chain
followed by the HTTP Client Shared Skill.

A redirect object records the ordered sequence of hops between an initial
[HTTP Request](http-request.md) and the final
[HTTP Response](http-response.md). It preserves the complete chain as evidence.

The HTTP Redirect object represents observed navigation only. It SHALL NOT
contain security interpretation or finding.

---

# Design Principles

An HTTP Redirect SHALL be

- Order preserving
- Complete
- Assessment scoped
- Evidence backed
- Explicit about termination
- Safe to reference

---

# Identity

Every HTTP Redirect SHALL contain

```yaml
redirect_id:

schema_version:
```

`redirect_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every HTTP Redirect SHALL contain

```yaml
assessment_id:

task_id:

transaction_id:
```

`assessment_id` identifies the owning assessment.

`task_id` identifies the task that authorized the request.

`transaction_id` SHALL reference the owning
[HTTP Transaction](http-transaction.md).

---

# Hops

Every HTTP Redirect SHALL contain

```yaml
hops:
```

`hops` SHALL be an ordered array of hop objects.

Each hop SHALL contain

```yaml
order:

from_url:

to_url:

status_code:

method:
```

`order` SHALL be a zero-based integer describing hop position.

`from_url` SHALL be the absolute URL that issued the redirect.

`to_url` SHALL be the absolute URL indicated by the `Location` header.

`status_code` SHALL be a redirection status code in the 3xx range.

`method` SHALL be the HTTP method used for the subsequent request.

---

# Method Changes

Each hop MAY contain

```yaml
method_changed:
```

`method_changed` SHALL be a boolean indicating that the method changed between
hops, for example a `POST` becoming a `GET` after a `303 See Other`.

---

# Chain Metadata

Every HTTP Redirect SHALL contain

```yaml
hop_count:

terminated_by:
```

`hop_count` SHALL equal the number of entries in `hops`.

`terminated_by` SHALL be one of

```
final_response

max_redirects

redirect_loop

policy

error
```

---

# Loop Detection

An HTTP Redirect MAY contain

```yaml
loop_detected:

loop_url:
```

`loop_detected` SHALL be a boolean indicating that a redirect loop was
identified.

`loop_url` SHALL be the URL at which the loop was detected when
`loop_detected` is `true`.

When `loop_detected` is `true`, `terminated_by` SHALL be `redirect_loop`.

---

# Final Response

An HTTP Redirect MAY contain

```yaml
final_response_id:
```

`final_response_id` SHALL reference the terminal
[HTTP Response](http-response.md) when `terminated_by` is `final_response`.

---

# Evidence

Every HTTP Redirect SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Redirect MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
redirect_id: httpredirect-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
task_id: task-042
transaction_id: httptxn-01
hops:
  - order: 0
    from_url: https://example.com/
    to_url: https://example.com/login
    status_code: 302
    method: GET
    method_changed: false
  - order: 1
    from_url: https://example.com/login
    to_url: https://example.com/dashboard
    status_code: 301
    method: GET
    method_changed: false
hop_count: 2
terminated_by: final_response
loop_detected: false
final_response_id: httpresp-01
evidence:
  - evidence-http-06
```

---

# Validation Rules

A valid HTTP Redirect object SHALL contain

- Redirect ID
- Schema Version
- Assessment ID
- Task ID
- Transaction ID
- Hops
- Hop Count
- Termination Reason
- Evidence References

A valid HTTP Redirect object SHALL satisfy

- `hop_count` equals the number of entries in `hops`
- Each hop `status_code` is in the 3xx range
- `terminated_by` is `redirect_loop` when `loop_detected` is `true`
- `final_response_id` is present when `terminated_by` is `final_response`
- No secret material appears in `extensions`

---

# Relationships

```
HTTP Redirect

├── HTTP Transaction
├── HTTP Response
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

- Cross-origin redirect classification
- Downgrade detection metadata
- Per-hop timing references

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Redirect object provides a complete, ordered record of a
redirect chain.

It enables domain skills to inspect navigation behavior while preserving the
full chain as evidence.
