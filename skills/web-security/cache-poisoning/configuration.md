# Web Cache Poisoning Configuration

**File:** `skills/web-security/cache-poisoning/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Web Cache Poisoning Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
cache_poisoning:

  checks:
    unkeyed_input:
    cache_reflection:
    response_splitting:

  probing:
    marker_ref:
    controlled_cache_key:
    candidate_inputs:

  limits:
    max_endpoints:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_cache_confirmation:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `unkeyed_input` — whether unkeyed influential inputs are checked. Default `true`.
- `cache_reflection` — whether unkeyed input reflection into cache is checked. Default
  `true`.
- `response_splitting` — whether header-based response splitting is checked. Default
  `true`.

---

## Probing

- `marker_ref` — a reference to a benign marker used to confirm reflection. It SHALL
  be benign only.
- `controlled_cache_key` — the controlled cache-key strategy used to isolate probes
  from real users' cache entries. It SHALL isolate testing from shared user-facing
  keys.
- `candidate_inputs` — the request inputs evaluated for cache influence.

---

## Limits

- `max_endpoints` — the maximum number of endpoints tested.
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

- `record_cache_confirmation` — whether controlled-cache-key confirmation is recorded
  in evidence. Default `true`.
- `redact_sensitive` — whether sensitive content is redacted. Default `true`.

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
- `marker_ref` SHALL be benign only.
- `controlled_cache_key` SHALL isolate testing from shared user-facing cache keys.
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
