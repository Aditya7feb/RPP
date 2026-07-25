# TLS Session Schema

**File:** `schemas/tls-session.md`

**Version:** 1.0.0

---

# Purpose

The TLS Session Schema defines the canonical representation of resumable TLS state observed or managed by the TLS Client.

A TLS Session SHALL contain metadata only.

Session secrets, ticket contents, pre-shared keys, and private keys SHALL NEVER be represented.

---

# Design Principles

A TLS Session SHALL be

- Assessment scoped
- Secret free
- Metadata only
- Isolation aware
- Adapter independent
- Safe to reference
- Explicit about resumption

---

# Identity

Every TLS Session SHALL contain

```yaml
session_id:

schema_version:
```

Session IDs SHALL be unique within an assessment.

Session IDs SHALL be 1 to 128 URI-safe characters.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every TLS Session SHALL contain

```yaml
assessment_id:
```

`assessment_id` identifies the owning assessment.

Sessions SHALL NOT cross assessment boundaries.

---

# Resumption Support

Every TLS Session SHALL contain

```yaml
resumption_supported:

resumption_attempted:

resumed:
```

`resumption_supported` indicates whether the peer and negotiated protocol indicated resumption support.

`resumption_attempted` indicates whether this connection attempted resumption.

`resumed` SHALL be true only when the handshake confirmed resumption.

`resumed` SHALL be false when `resumption_attempted` is false.

---

# Mechanism

Every TLS Session SHALL contain

```yaml
mechanism:
```

Allowed values

```
none

session_id

session_ticket

psk
```

`none` SHALL be used when resumption is unsupported.

---

# Isolation Scope

Every TLS Session SHALL contain

```yaml
isolation_scope:
```

Allowed values

```
connection

task

assessment
```

The isolation scope SHALL NOT exceed assessment scope.

---

# Timing

Every TLS Session SHALL contain

```yaml
created_at:
```

TLS Sessions MAY contain

```yaml
expires_at:
```

Timestamps SHALL be RFC 3339 UTC timestamps.

`expires_at` SHALL be later than `created_at` when present.

---

# Server Name

TLS Sessions MAY contain

```yaml
server_name:
```

`server_name` SHALL be the DNS hostname used for SNI.

DNS names SHALL be normalized to lowercase.

`server_name` SHALL NOT be an IP literal.

---

# Extensions

TLS Sessions MAY contain

```yaml
extensions:
```

Extensions SHALL contain namespaced, non-secret adapter metadata.

Extensions SHALL NOT contain session secrets, ticket contents, pre-shared keys, or private keys.

---

# Example

```yaml
session_id: tlssession-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
resumption_supported: true
resumption_attempted: true
resumed: true
mechanism: session_ticket
isolation_scope: assessment
created_at: '2026-07-25T10:00:01Z'
expires_at: '2026-07-25T18:00:01Z'
server_name: api.example.com
```

---

# Validation Rules

A valid TLS Session object SHALL contain

- Session ID
- Schema Version
- Assessment ID
- Resumption Supported Status
- Resumption Attempted Status
- Resumed Status
- Mechanism
- Isolation Scope
- Creation Timestamp

---

# Success Criteria

A compliant TLS Session object records reusable TLS session metadata without exposing secrets.

It enables controlled session reuse while preserving assessment isolation, evidence safety, and adapter independence.
