# Cross-Site Scripting Configuration

**File:** `skills/web-security/xss/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Cross-Site Scripting Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
xss:

  checks:
    reflected:
    stored:
    dom_based:
    context_encoding:

  payloads:
    payload_set_ref:
    max_payloads_per_point:

  rendering:
    observe_execution:

  limits:
    max_injection_points:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_marker:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `reflected` — whether reflected XSS is checked. Default `true`.
- `stored` — whether stored XSS is checked. Stored testing persists input and is
  higher impact. Default `false` unless authorized.
- `dom_based` — whether DOM-based XSS is checked. Default `true`.
- `context_encoding` — whether context-appropriate encoding is assessed. Default
  `true`.

---

## Payloads

- `payload_set_ref` — a reference to a managed set of bounded marker payloads. It
  SHALL be a reference, never inline weaponized payloads.
- `max_payloads_per_point` — the maximum number of markers tried per injection point.

---

## Rendering

- `observe_execution` — whether marker execution is observed through the Browser.
  Default `true`.

---

## Limits

- `max_injection_points` — the maximum number of injection points tested.
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

- `record_marker` — whether the confirming marker is recorded in evidence. Default
  `true`.
- `redact_sensitive` — whether sensitive surrounding content is redacted. Default
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
- `payload_set_ref` SHALL be a reference, never inline weaponized payloads.
- `stored` SHALL require authorization consistent with the Rules of Engagement.
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
