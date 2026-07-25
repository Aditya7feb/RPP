# Mutual TLS Authentication Configuration

**File:** `skills/authentication/mtls/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Mutual TLS
Authentication Skill and the precedence rules that resolve it. Configuration is
data; it never contains implementation logic.

---

# Configuration Object

```yaml
mtls_authentication:

  checks:
    certificate_required:
    untrusted_certificate_acceptance:
    expired_certificate_acceptance:
    unexpected_ca_acceptance:
    identity_binding:
    revocation_checking:
    fallback_detection:

  client_certificate:
    client_certificate_ref:
    variants:

  limits:
    max_connections:
    handshake_timeout_ms:

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

- `certificate_required` — whether client-certificate requirement is checked.
  Default `true`.
- `untrusted_certificate_acceptance` — whether acceptance of untrusted or
  self-signed certificates is checked. Default `true`.
- `expired_certificate_acceptance` — whether acceptance of expired certificates is
  checked. Default `true`.
- `unexpected_ca_acceptance` — whether acceptance of certificates from an
  unexpected authority is checked. Default `true`.
- `identity_binding` — whether certificate subject or SAN binding is checked.
  Default `true`.
- `revocation_checking` — whether revocation checking is checked. Default `true`.
- `fallback_detection` — whether fallback to weaker authentication is checked.
  Default `true`.

---

## Client Certificate

- `client_certificate_ref` — a reference to a managed test client certificate and
  key. It SHALL be a reference, never inline key material.
- `variants` — references to managed certificate variants used for validation
  checks, such as expired or untrusted certificates. Each SHALL be a reference.

---

## Limits

- `max_connections` — the maximum number of handshakes.
- `handshake_timeout_ms` — per-handshake timeout in milliseconds.

---

## Rate

- `respect_policy_ceiling` — whether the Policy Engine rate ceiling is honored.
  Default `true` and SHALL NOT be disabled in enforcing environments.
- `max_requests_per_second` — a self-imposed ceiling at or below the policy
  ceiling.

---

## Evidence

- `redact_secrets` — whether private key material is redacted in evidence. Default
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
- `client_certificate_ref` and each variant SHALL be references, never inline key
  material.
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
- [Certificate Schema](../../../schemas/certificate.md)
