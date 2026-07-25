# CSRF Protection Configuration

**File:** `skills/authentication/csrf/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the CSRF Protection Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
csrf_protection:

  checks:
    token_presence:
    token_validation:
    session_binding:
    same_site:
    origin_check:
    safe_method_state_change:

  authentication:
    credentials_ref:
    login_endpoint:

  targets:
    state_changing_endpoints:

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

- `token_presence` — whether anti-CSRF token presence is checked. Default `true`.
- `token_validation` — whether server-side token validation is checked. Default
  `true`.
- `session_binding` — whether token session binding is checked. Default `true`.
- `same_site` — whether same-site cookie protection is checked. Default `true`.
- `origin_check` — whether origin or referer validation is checked. Default `true`.
- `safe_method_state_change` — whether state changes via safe methods are checked.
  Default `true`.

---

## Authentication

- `credentials_ref` — a reference to managed test credentials. It SHALL be a
  reference, never inline secrets.
- `login_endpoint` — the endpoint used to reach an authenticated state.

---

## Targets

- `state_changing_endpoints` — the endpoints evaluated for CSRF protection.

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

- `redact_secrets` — whether anti-CSRF tokens are redacted in evidence. Default
  `true` and SHALL NOT be disabled.

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
- `credentials_ref` SHALL be a reference, never inline secrets.
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
