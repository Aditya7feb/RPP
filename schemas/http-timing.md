# HTTP Timing Schema

**File:** `schemas/http-timing.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Timing Schema defines the canonical representation of timing metrics
collected for one HTTP exchange by the HTTP Client Shared Skill.

Timing metrics describe the duration of each phase of a request, from DNS
resolution through response completion. Every [HTTP Response](http-response.md)
and [HTTP Transaction](http-transaction.md) references an HTTP Timing object.

The HTTP Timing object represents measured durations only. It SHALL NOT contain
security interpretation or finding.

---

# Design Principles

An HTTP Timing SHALL be

- Phase aware
- Consistent in units
- Assessment scoped
- Evidence backed
- Adapter independent
- Safe to reference

---

# Identity

Every HTTP Timing SHALL contain

```yaml
timing_id:

schema_version:
```

`timing_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every HTTP Timing SHALL contain

```yaml
assessment_id:

transaction_id:
```

`assessment_id` identifies the owning assessment.

`transaction_id` SHALL reference the owning
[HTTP Transaction](http-transaction.md).

---

# Units

Every HTTP Timing SHALL contain

```yaml
unit:
```

`unit` SHALL be `milliseconds`.

All phase durations SHALL be expressed in the declared unit as non-negative
numbers.

---

# Phase Durations

An HTTP Timing MAY contain

```yaml
dns:

connect:

tls:

send:

wait:

receive:
```

`dns` SHALL be the time to resolve the target host.

`connect` SHALL be the time to establish the transport connection.

`tls` SHALL be the time to complete the TLS handshake when HTTPS is used.

`send` SHALL be the time to transmit the request.

`wait` SHALL be the time between request completion and the first response byte.

`receive` SHALL be the time to read the complete response.

A phase SHALL be omitted when it does not apply, for example `tls` for a plain
HTTP request.

---

# Totals

Every HTTP Timing SHALL contain

```yaml
total:
```

`total` SHALL be the end-to-end duration of the exchange.

`total` SHOULD be greater than or equal to the sum of the recorded phases.

---

# Timestamps

An HTTP Timing MAY contain

```yaml
started_at:

completed_at:
```

`started_at` SHALL be an RFC 3339 UTC timestamp marking request initiation.

`completed_at` SHALL be an RFC 3339 UTC timestamp on or after `started_at`.

---

# Retry Timing

An HTTP Timing MAY contain

```yaml
retry_delay:

attempt:
```

`retry_delay` SHALL be the delay applied before this attempt when the exchange
was retried.

`attempt` SHALL be a one-based integer identifying the attempt number.

---

# Evidence

Every HTTP Timing SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Timing MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
timing_id: httptiming-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
transaction_id: httptxn-01
unit: milliseconds
dns: 12
connect: 30
tls: 45
send: 3
wait: 210
receive: 18
total: 320
started_at: '2026-07-25T10:00:00.000Z'
completed_at: '2026-07-25T10:00:00.320Z'
attempt: 1
evidence:
  - evidence-http-07
```

---

# Validation Rules

A valid HTTP Timing object SHALL contain

- Timing ID
- Schema Version
- Assessment ID
- Transaction ID
- Unit
- Total
- Evidence References

A valid HTTP Timing object SHALL satisfy

- `unit` is `milliseconds`
- All recorded phase durations are non-negative
- `total` is greater than or equal to the sum of recorded phases
- `completed_at`, when present, is on or after `started_at`
- No secret material appears in `extensions`

---

# Relationships

```
HTTP Timing

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

- Per-hop redirect timing
- Connection pool acquisition timing
- Protocol negotiation timing
- Server timing header correlation

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Timing object provides a consistent, phase-aware record of the
duration of one HTTP exchange.

It enables observability and performance analysis across every transport adapter
while preserving timing as evidence.
