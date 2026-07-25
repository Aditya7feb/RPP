# Clickjacking Configuration

**File:** `skills/web-security/clickjacking/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Clickjacking Skill and
the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
clickjacking:

  checks:
    x_frame_options:
    frame_ancestors:
    page_sensitivity:

  targets:
    sensitive_endpoints:

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

- `x_frame_options` — whether the `X-Frame-Options` header is checked. Default
  `true`.
- `frame_ancestors` — whether the CSP `frame-ancestors` directive is checked.
  Default `true`.
- `page_sensitivity` — whether page sensitivity is assessed. Default `true`.

---

## Targets

- `sensitive_endpoints` — the endpoints prioritized for framing-protection
  evaluation.

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

- `capture_headers` — whether relevant response headers are captured in evidence.
  Default `true`.

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
