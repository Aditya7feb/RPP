# HTTP Session Schema

**File:** `schemas/http-session.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Session Schema defines the canonical representation of an HTTP session
managed by the HTTP Client Shared Skill.

A session groups related HTTP transactions and preserves state such as cookies,
authentication, and connection reuse across multiple requests. Sessions are
created, cloned, and closed through the `CreateSession`, `CloneSession`, and
`CloseSession` operations defined in
[the HTTP Client interface](../skills/shared/http-client/interface.md).

The HTTP Session object represents state only. It SHALL NOT contain security
interpretation or finding.

---

# Design Principles

An HTTP Session SHALL be

- Assessment scoped
- Isolated by default
- Lifecycle aware
- State preserving
- Evidence backed
- Free of embedded secrets

---

# Identity

Every HTTP Session SHALL contain

```yaml
session_id:

schema_version:
```

`session_id` SHALL be unique within an assessment.

`schema_version` SHALL be `1.0.0`.

---

# Assessment Relationship

Every HTTP Session SHALL contain

```yaml
assessment_id:

task_id:
```

`assessment_id` identifies the owning assessment.

`task_id` identifies the task that created the session.

---

# Lifecycle State

Every HTTP Session SHALL contain

```yaml
state:

created_at:
```

Allowed states

```
active

idle

expired

closed
```

`created_at` SHALL be an RFC 3339 UTC timestamp.

---

# Closure Metadata

An HTTP Session MAY contain

```yaml
closed_at:

expires_at:
```

`closed_at` SHALL be an RFC 3339 UTC timestamp on or after `created_at`.

`closed_at` SHALL be present when `state` is `closed`.

`expires_at` SHALL be an RFC 3339 UTC timestamp describing session expiration.

---

# Cookie Store

An HTTP Session MAY contain

```yaml
cookies:
```

`cookies` SHALL be an array of [HTTP Cookie](http-cookie.md) references owned by
the session.

The cookie store SHALL remain scoped to the session unless explicitly shared.

---

# Authentication

An HTTP Session MAY contain

```yaml
authentication_profile:

authenticated:
```

`authentication_profile` SHALL reference a shared
[Authentication](../skills/shared/authentication/README.md) profile.

`authenticated` SHALL be a boolean indicating whether the session currently
holds valid authentication state.

Credentials SHALL NEVER be embedded directly in the session object.

---

# CSRF State

An HTTP Session MAY contain

```yaml
csrf_tokens:
```

`csrf_tokens` SHALL be an array of token references maintained for the session.

Token values SHALL be redacted in exported evidence.

---

# Connection Reuse

An HTTP Session MAY contain

```yaml
keep_alive:

connection_pool_id:
```

`keep_alive` SHALL be a boolean indicating whether persistent connections are
enabled for the session.

`connection_pool_id` SHALL reference the connection pool used by the session
when connection reuse is active.

---

# Isolation

Every HTTP Session SHALL contain

```yaml
isolation_scope:
```

`isolation_scope` SHALL be one of

```
assessment

task

request
```

Sessions SHALL NOT share state across isolation boundaries unless explicitly
configured through `CloneSession`.

---

# Origin

An HTTP Session MAY contain

```yaml
cloned_from:
```

`cloned_from` SHALL reference the parent `session_id` when the session was
produced by `CloneSession`.

A cloned session SHALL copy cookie and authentication state while receiving a
new `session_id`.

---

# Transactions

An HTTP Session MAY contain

```yaml
transactions:
```

`transactions` SHALL be an array of
[HTTP Transaction](http-transaction.md) references executed within the session.

---

# Evidence

Every HTTP Session SHALL contain

```yaml
evidence:
```

`evidence` SHALL be an array of Evidence IDs conforming to
[evidence.md](evidence.md).

`evidence` MAY be empty only before collection.

---

# Extensions

An HTTP Session MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced adapter metadata.

`extensions` SHALL NOT contain secrets.

---

# Example

```yaml
session_id: httpsession-01
schema_version: 1.0.0
assessment_id: assessment-2026-001
task_id: task-042
state: active
created_at: '2026-07-25T10:00:00Z'
expires_at: '2026-07-25T11:00:00Z'
cookies:
  - httpcookie-01
authentication_profile: cms-admin
authenticated: true
csrf_tokens:
  - csrf-ref-01
keep_alive: true
connection_pool_id: pool-01
isolation_scope: assessment
transactions:
  - httptxn-01
evidence:
  - evidence-http-04
```

---

# Validation Rules

A valid HTTP Session object SHALL contain

- Session ID
- Schema Version
- Assessment ID
- Task ID
- State
- Created Timestamp
- Isolation Scope
- Evidence References

A valid HTTP Session object SHALL satisfy

- `state` is one of the allowed states
- `closed_at` is present when `state` is `closed`
- `isolation_scope` is one of the allowed scopes
- No secret material appears in `csrf_tokens`, `cookies`, or `extensions`

---

# Relationships

```
HTTP Session

├── HTTP Cookie
├── HTTP Transaction
├── Authentication Profile
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

- Storage partitions
- Origin isolation policies
- Session replication metadata
- Distributed session state

Backward compatibility SHOULD be maintained through `extensions`.

---

# Success Criteria

A compliant HTTP Session object provides a complete, isolated record of HTTP
session state.

It enables the HTTP Client to preserve cookies, authentication, and connection
reuse across transactions while maintaining strict isolation boundaries.
