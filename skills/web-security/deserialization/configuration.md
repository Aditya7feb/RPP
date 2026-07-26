# Insecure Deserialization Configuration

**File:** `skills/web-security/deserialization/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Insecure Deserialization
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
deserialization:

  checks:
    out_of_band_interaction:
    response_differential:
    type_restriction:

  probes:
    payload_set_ref:
    max_probes_per_endpoint:

  out_of_band:
    collector_ref:

  limits:
    max_endpoints:
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
  `false` unless a controlled collector is provided.
- `response_differential` — whether response or timing differentials are checked.
  Default `true`.
- `type_restriction` — whether missing type restrictions are assessed. Default
  `true`.

---

## Probes

- `payload_set_ref` — a reference to a managed set of bounded serialized probes. It
  SHALL be a reference, never a functional gadget chain.
- `max_probes_per_endpoint` — the maximum number of probes tried per endpoint.

---

## Out Of Band

- `collector_ref` — a reference to a controlled out-of-band collector. It SHALL
  reference an authorized collector only.

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

- `record_interaction` — whether the bounded probe interaction is recorded in
  evidence. Default `true`.
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
- `payload_set_ref` SHALL be a reference, never a functional gadget chain.
- `collector_ref` SHALL reference an authorized collector only.
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
