# CORS Configuration

**File:** `skills/web-security/cors/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the CORS Skill and the
precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
cors:

  checks:
    origin_reflection:
    null_origin:
    credentialed_access:
    wildcard_with_credentials:
    permissive_methods_headers:
    weak_origin_validation:

  probing:
    test_origins:

  limits:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    capture_headers:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `origin_reflection` — whether arbitrary-origin reflection is checked. Default
  `true`.
- `null_origin` — whether `null` origin acceptance is checked. Default `true`.
- `credentialed_access` — whether credentialed cross-origin access is checked.
  Default `true`.
- `wildcard_with_credentials` — whether wildcard-with-credentials is checked.
  Default `true`.
- `permissive_methods_headers` — whether permissive methods and headers are checked.
  Default `true`.
- `weak_origin_validation` — whether substring or suffix validation flaws are
  checked. Default `true`.

---

## Probing

- `test_origins` — the untrusted origins used to probe reflection behavior. Each
  SHALL be used only for observation, never for exploitation.

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

- `capture_headers` — whether cross-origin response headers are captured in
  evidence. Default `true`.

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
- Numeric limits SHALL be positive.
- `max_requests_per_second` SHALL NOT exceed the policy ceiling.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
