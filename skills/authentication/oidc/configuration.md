# OIDC Authentication Configuration

**File:** `skills/authentication/oidc/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the OIDC Authentication Skill
and the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
oidc_authentication:

  checks:
    id_token_signature:
    audience_issuer_validation:
    nonce_enforcement:
    discovery_document:
    jwks_exposure:
    userinfo_handling:
    identity_claim_trust:

  client:
    client_credentials_ref:
    expected_issuer:

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

- `id_token_signature` — whether ID token signature validation is checked. Default
  `true`.
- `audience_issuer_validation` — whether audience and issuer validation is checked.
  Default `true`.
- `nonce_enforcement` — whether nonce enforcement is checked. Default `true`.
- `discovery_document` — whether the discovery document is checked. Default `true`.
- `jwks_exposure` — whether JWKS exposure is checked. Default `true`.
- `userinfo_handling` — whether UserInfo handling is checked. Default `true`.
- `identity_claim_trust` — whether identity-claim verification is checked. Default
  `true`.

---

## Client

- `client_credentials_ref` — a reference to managed test client credentials. It
  SHALL be a reference, never inline secrets.
- `expected_issuer` — the issuer identifier expected for validation checks.

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

- `redact_secrets` — whether ID tokens and secrets are redacted in evidence.
  Default `true` and SHALL NOT be disabled.

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
- `client_credentials_ref` SHALL be a reference, never inline secrets.
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
