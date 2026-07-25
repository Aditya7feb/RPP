# OAuth2 Authentication Configuration

**File:** `skills/authentication/oauth2/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the OAuth2 Authentication
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
oauth2_authentication:

  checks:
    redirect_uri_validation:
    state_parameter:
    pkce_enforcement:
    grant_type_hygiene:
    token_transport:
    scope_enforcement:

  client:
    client_credentials_ref:
    redirect_uris:
    grant_types:

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

- `redirect_uri_validation` — whether redirect-URI validation is checked. Default
  `true`.
- `state_parameter` — whether anti-forgery `state` usage is checked. Default
  `true`.
- `pkce_enforcement` — whether PKCE enforcement is checked. PKCE SHOULD be enforced
  for all Authorization Code clients, including both public and confidential
  clients. Default `true`.
- `grant_type_hygiene` — whether discouraged grant types are checked. Default
  `true`.
- `token_transport` — whether secure token transport is checked. Default `true`.
- `scope_enforcement` — whether scope enforcement is checked. Default `true`.

---

## Client

- `client_credentials_ref` — a reference to managed test client credentials. It
  SHALL be a reference, never inline secrets.
- `redirect_uris` — the registered redirect URIs used for validation checks.
- `grant_types` — the grant types under evaluation.

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

- `redact_secrets` — whether tokens and client secrets are redacted in evidence.
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
- [HTTP Redirect Schema](../../../schemas/http-redirect.md)
