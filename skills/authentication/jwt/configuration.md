# JWT Authentication Configuration

**File:** `skills/authentication/jwt/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the JWT Authentication Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
jwt_authentication:

  checks:
    unsigned_acceptance:
    algorithm_confusion:
    signature_validation:
    expiry_enforcement:
    issuer_audience_validation:
    payload_confidentiality:
    transport_security:

  secret_analysis:
    enabled:
    max_candidates:
    dictionary_ref:

  token:
    token_ref:
    injection_points:

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

- `unsigned_acceptance` — whether acceptance of unsigned tokens is checked. Default
  `true`.
- `algorithm_confusion` — whether algorithm confusion is checked. Default `true`.
- `signature_validation` — whether signature verification is checked. Default
  `true`.
- `expiry_enforcement` — whether expiry enforcement is checked. Default `true`.
- `issuer_audience_validation` — whether issuer and audience validation is checked.
  Default `true`.
- `payload_confidentiality` — whether payload data disclosure is checked. Default
  `true`.
- `transport_security` — whether token transport is checked. Default `true`.

---

## Secret Analysis

- `enabled` — whether bounded weak-secret analysis is performed. Default `false`.
- `max_candidates` — the maximum number of candidate secrets evaluated. It SHALL be
  bounded and SHALL respect the Rules of Engagement.
- `dictionary_ref` — a reference to a managed candidate dictionary. It SHALL be a
  reference, never inline content.

---

## Token

- `token_ref` — a reference to a managed test token. It SHALL be a reference, never
  an inline token.
- `injection_points` — the header or parameter locations where tokens are supplied.

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

- `redact_secrets` — whether token secrets and full tokens are redacted in
  evidence. Default `true` and SHALL NOT be disabled.

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
- `token_ref` and `dictionary_ref` SHALL be references, never inline content.
- `secret_analysis.max_candidates` SHALL be bounded and positive when enabled.
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
