# API Key Authentication Configuration

**File:** `skills/authentication/api-keys/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the API Key Authentication
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
api_key_authentication:

  checks:
    url_exposure:
    client_exposure:
    transport_security:
    server_validation:
    scope_and_lifecycle:

  key:
    api_key_ref:
    placement_candidates:

  limits:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    redact_secrets:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `url_exposure` — whether keys in URLs or query strings are checked. Default
  `true`.
- `client_exposure` — whether keys exposed in client code are checked. Default
  `true`.
- `transport_security` — whether key transport is checked. Default `true`.
- `server_validation` — whether server-side validation is checked. Default `true`.
- `scope_and_lifecycle` — whether key scope, expiry, and rotation are checked.
  Default `true`.

---

## Key

- `api_key_ref` — a reference to a managed test key. It SHALL be a reference, never
  an inline key.
- `placement_candidates` — the header, query, or body placements to observe.

---

## Limits

- `max_requests` — the maximum number of requests.
- `request_timeout_ms` — per-request timeout in milliseconds.

---

## Rate

- `respect_policy_ceiling` — whether the Policy Engine rate ceiling is honored.
  Default `true` and SHALL NOT be disabled in enforcing environments.
- `max_requests_per_second` — a self-imposed ceiling at or below the policy
  ceiling.

---

## Evidence

- `redact_secrets` — whether key material is redacted in evidence. Default `true`
  and SHALL NOT be disabled.

---

## Policy

- `scope_id` — the [Scope](../../../schemas/scope.md) reference.
- `roe_id` — the [Rules of Engagement](../../../schemas/rules-of-engagement.md)
  reference.

---

# Precedence

Configuration resolves in the following order, later overriding earlier, except
that policy constraints SHALL NOT be weakened:

```
Skill Defaults

↓

Assessment Configuration

↓

Request Parameters

↓

Policy Engine Constraints (highest, may only tighten)
```

The [Policy Engine](../../shared/policy-engine/README.md) rate ceiling and scope
decision SHALL always take precedence.

---

# Validation Rules

- `scope_id` and `roe_id` SHALL be present.
- `api_key_ref` SHALL be a reference, never an inline key.
- Numeric limits SHALL be positive.
- `max_requests_per_second` SHALL NOT exceed the policy ceiling.
- `redact_secrets` SHALL NOT be disabled.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
