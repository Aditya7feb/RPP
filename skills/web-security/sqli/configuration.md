# SQL Injection Configuration

**File:** `skills/web-security/sqli/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the SQL Injection Skill and
the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
sql_injection:

  checks:
    error_based:
    boolean_based:
    time_based:

  probes:
    payload_set_ref:
    max_probes_per_point:

  time_based:
    max_delay_ms:

  limits:
    max_injection_points:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_signal:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `error_based` — whether error-based injection is checked. Default `true`.
- `boolean_based` — whether boolean-based blind injection is checked. Default
  `true`.
- `time_based` — whether time-based blind injection is checked. Default `true`.

---

## Probes

- `payload_set_ref` — a reference to a managed set of bounded probes. It SHALL be a
  reference, never inline data-extraction payloads.
- `max_probes_per_point` — the maximum number of probes tried per injection point.

---

## Time Based

- `max_delay_ms` — the maximum induced delay for time-based confirmation. It SHALL
  be bounded to avoid disruption.

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

- `record_signal` — whether the confirming signal is recorded in evidence. Default
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
- `payload_set_ref` SHALL be a reference, never inline data-extraction payloads.
- `max_delay_ms` SHALL be bounded and positive.
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
