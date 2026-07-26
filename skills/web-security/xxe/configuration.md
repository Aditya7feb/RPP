# XML External Entity Configuration

**File:** `skills/web-security/xxe/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the XML External Entity Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
xxe:

  checks:
    in_band_resolution:
    out_of_band_resolution:
    dtd_configuration:

  probes:
    marker_ref:
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
    record_resolution:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `in_band_resolution` — whether in-band, non-sensitive resolution is checked.
  Default `true`.
- `out_of_band_resolution` — whether out-of-band resolution is checked. Default
  `false` unless a controlled collector is provided.
- `dtd_configuration` — whether unsafe document-type-definition configuration is
  assessed. Default `true`.

---

## Probes

- `marker_ref` — a reference to a non-sensitive resource used to confirm resolution.
  It SHALL NOT reference a sensitive file.
- `max_probes_per_endpoint` — the maximum number of probes tried per endpoint.

---

## Out Of Band

- `collector_ref` — a reference to a controlled out-of-band collector. It SHALL
  reference an authorized collector only.

---

## Limits

- `max_endpoints` — the maximum number of XML endpoints tested.
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

- `record_resolution` — whether the non-sensitive resolution signal is recorded in
  evidence. Default `true`.
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
- `marker_ref` SHALL reference a non-sensitive resource only.
- `collector_ref` SHALL reference an authorized collector only.
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
