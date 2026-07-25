# Cache Examples

**File:** `skills/shared/cache/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Cache Shared Skill in use.

Examples demonstrate consumers, keys, freshness, revalidation, scope, evidence,
and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — DNS Resolution Cache Hit

A discovery skill resolves the same host multiple times within an assessment.

## Invocation

```yaml
metadata:
  request_id: req-3001
  assessment_id: asmt-42
  task_id: task-subdomain-enum
  skill_id: subdomain-discovery
namespace: dns
operation: resolve
parameters:
  name: api.example.com
  type: A
scope: assessment
producer: <dns-resolve-callback>
cacheable: true
ttl: 300s
```

## First Call

```yaml
outcome: miss_stored
value: [ 93.184.216.34 ]
entry_ref: cache-dns-0001
```

## Second Call Within TTL

```yaml
outcome: hit
value: [ 93.184.216.34 ]
freshness:
  expires_at: 2026-07-25T11:35:00Z
```

The second resolution is served from cache without a network operation.

---

# Example 2 — Stale-While-Revalidate

A TLS metadata lookup serves a stale value while revalidating.

## Configuration

```yaml
defaults:
  ttl: 600s
  stale_while_revalidate: 60s
```

## Behavior After Expiry Within The Window

```yaml
outcome: stale_hit
value: <cached-tls-metadata>
revalidation: triggered
```

The consumer receives the stale value immediately while a fresh value is
obtained in the background.

---

# Example 3 — Conditional Revalidation

An HTTP GET result carries a validator and is revalidated.

## Stored Entry Validators

```yaml
validators:
  etag: "abc123"
```

## Revalidation Outcome

```yaml
outcome: revalidated
freshness:
  refreshed: true
```

The producer confirms the entry using the validator, and freshness is refreshed
without transferring the full value.

---

# Example 4 — Non-Cacheable Authenticated Response

An authenticated response containing session data is not cached.

## Invocation

```yaml
namespace: http
operation: get
parameters:
  url: https://app.example.com/account
scope: session
cacheable: false
```

## Result

```yaml
outcome: miss_uncached
value: <response>
```

The value is returned to the caller but not stored, preventing leakage of
sensitive data.

---

# Example 5 — Scope Isolation

A `session` entry is not served to a different session.

## Behavior

```
Session A stores entry (scope: session)

↓

Session B lookup same key

↓

outcome: miss_stored   # isolated per session
```

Scope isolation prevents cross-session reuse.

---

# Example 6 — Backend Unavailable Degrades To Miss

The cache backend is temporarily unavailable.

## Result

```yaml
outcome: miss_uncached
value: <freshly-produced-value>
degraded: true
```

Correctness is preserved: the producer yields a fresh value even though caching
is unavailable.

---

# Example 7 — Evidence Record

A single lookup produces the following evidence.

```yaml
evidence:
  type: cache-lookup
  namespace: dns
  key: dns:resolve:9f2c1a
  decision: hit
  scope: assessment
  produced_by: dns-client
  decided_at: 2026-07-25T11:32:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes cached secrets, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)
- [DNS Client](../dns-client/README.md)
