# Server-Side Request Forgery Configuration

**File:** `skills/web-security/ssrf/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Server-Side Request Forgery
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
ssrf:

  checks:
    out_of_band_interaction:
    response_differential:
    destination_validation:

  probing:
    collector_ref:
    candidate_parameters:

  limits:
    max_parameters:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_interaction:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `out_of_band_interaction` — whether out-of-band confirmation is checked. Default
  `true` where a controlled collector is provided.
- `response_differential` — whether response or timing differentials are checked.
  Default `true`.
- `destination_validation` — whether destination-validation flaws are assessed.
  Default `true`.

---

## Probing

- `collector_ref` — a reference to a controlled out-of-band collector. It SHALL
  reference an authorized collector only.
- `candidate_parameters` — the request-issuing parameters evaluated.

---

## Limits

- `max_parameters` — the maximum number of parameters tested.
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

- `record_interaction` — whether the controlled-destination interaction is recorded
  in evidence. Default `true`.
- `redact_sensitive` — whether any incidental sensitive content is redacted. Default
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
- `collector_ref` SHALL reference an authorized collector only.
- Destinations SHALL be controlled or benign; internal-address targeting SHALL NOT be
  configured.
- Numeric limits SHALL be positive.
- `max_requests_per_second` SHALL NOT exceed the policy ceiling.
- `redact_sensitive` SHALL NOT be disabled.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
