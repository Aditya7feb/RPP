# Content Security Policy Configuration

**File:** `skills/web-security/csp/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Content Security Policy
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
content_security_policy:

  checks:
    policy_presence:
    unsafe_inline_eval:
    broad_sources:
    directive_coverage:
    known_bypasses:
    enforcement_mode:

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

- `policy_presence` — whether CSP presence is checked. Default `true`.
- `unsafe_inline_eval` — whether `unsafe-inline` and `unsafe-eval` are checked.
  Default `true`.
- `broad_sources` — whether wildcard or overly broad sources are checked. Default
  `true`.
- `directive_coverage` — whether key directive coverage is checked. Default `true`.
- `known_bypasses` — whether known allow-list bypasses are checked. Default `true`.
- `enforcement_mode` — whether enforcing versus report-only mode is checked.
  Default `true`.

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

- `capture_headers` — whether the CSP header is captured in evidence. Default
  `true`.

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
