# Secrets Client Examples

**File:** `skills/shared/secrets-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Secrets Client Shared Skill in use.

Examples demonstrate handle resolution, brokered application, rotation, denial,
non-sensitive evidence, and expected outputs.

All examples are illustrative and contain no implementation code, and no example
contains a secret value.

---

# Example 1 — Resolve An Opaque Handle

The Authentication package resolves a handle for later brokered use.

## Invocation

```yaml
metadata:
  request_id: req-9901
  assessment_id: asmt-42
  task_id: task-auth-setup
  skill_id: authentication
secret_ref: engagement-vault/api-token-shop
mode: resolve_handle
```

## Result

```yaml
outcome: resolved
handle: secret-handle-7f2a
lease:
  lease_id: lease-1a2b
  expires_at: 2026-07-25T17:45:00Z
version: "4"
```

The result contains an opaque handle, never the value.

---

# Example 2 — Brokered Application

A secret is applied to an outbound request header without exposing it.

## Invocation

```yaml
secret_ref: engagement-vault/api-token-shop
mode: broker_apply
broker_target:
  kind: http_header
  name: authorization
```

## Result

```yaml
outcome: brokered
evidence:
  purpose: outbound-authentication
  applied: true
```

The value is applied at the point of use by the
[Authentication](../authentication/README.md) broker; the requesting skill never
sees it.

---

# Example 3 — Rotation Tolerated

The secret rotates; the handle reflects the new version transparently.

## Behavior

```
version 4 → rotation detected → version 5

handle continues to broker the current version
```

Consumers using handles tolerate rotation without cached values.

---

# Example 4 — Access Denied

Access to a secret is denied by store policy.

## Result

```yaml
outcome: denied
error:
  category: Authorization
  code: denied
  secret_ref: engagement-vault/db-root
  retryable: false
```

The error reveals no value and no more existence detail than the store permits.

---

# Example 5 — Expired Handle

An expired handle is re-resolved.

## Result

```yaml
outcome: expired
error:
  category: Lease
  code: expired
  retryable: true
```

The consumer re-resolves the reference to obtain a fresh handle.

---

# Example 6 — Value Return Refused

A caller requests a raw value.

## Result

```yaml
outcome: denied
error:
  category: Validation
  code: value_supplied
  retryable: false
```

The interface never returns secret values to general consumers.

---

# Example 7 — Non-Sensitive Evidence Record

A single access produces the following non-sensitive evidence.

```yaml
evidence:
  type: secret-access
  secret_ref: engagement-vault/api-token-shop
  version: "4"
  purpose: outbound-authentication
  outcome: brokered
  decided_at: 2026-07-25T17:30:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md) and contains no secret value.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
