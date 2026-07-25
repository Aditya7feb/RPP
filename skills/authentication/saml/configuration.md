# SAML Authentication Configuration

**File:** `skills/authentication/saml/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the SAML Authentication Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
saml_authentication:

  checks:
    unsigned_assertion:
    signature_stripping:
    signature_wrapping:
    audience_restriction:
    recipient_destination:
    replay_protection:
    transport_security:

  assertion:
    assertion_ref:
    variants:

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

- `unsigned_assertion` — whether acceptance of unsigned assertions is checked.
  Default `true`.
- `signature_stripping` — whether signature stripping is checked. Default `true`.
- `signature_wrapping` — whether XML signature wrapping is checked. Default `true`.
- `audience_restriction` — whether audience restriction enforcement is checked.
  Default `true`.
- `recipient_destination` — whether recipient and destination validation is checked.
  Default `true`.
- `replay_protection` — whether replay protection is checked. Default `true`.
- `transport_security` — whether assertion transport is checked. Default `true`.

---

## Assertion

- `assertion_ref` — a reference to a managed test assertion and signing material. It
  SHALL be a reference, never inline material.
- `variants` — references to managed assertion variants used for validation checks,
  such as unsigned or wrapped assertions. Each SHALL be a reference.

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

- `redact_secrets` — whether assertions and signing material are redacted in
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
- `assertion_ref` and each variant SHALL be references, never inline material.
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
