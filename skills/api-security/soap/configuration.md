# SOAP API Security Configuration

**File:** `skills/api-security/soap/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the SOAP API Security Skill and
the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
soap_api_security:

  checks:
    wsdl_exposure:
    ws_security_enforcement:
    action_authorization:
    message_integrity:
    verbose_faults:

  identities:
    identities_ref:

  wsdl:
    wsdl_ref:

  limits:
    max_operations:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    minimal_confirmation:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `wsdl_exposure` — whether WSDL and operation exposure is checked. Default `true`.
- `ws_security_enforcement` — whether WS-Security enforcement is checked. Default
  `true`.
- `action_authorization` — whether SOAP action and operation-level authorization is
  checked. Default `true`.
- `message_integrity` — whether message-level signature or integrity validation is
  checked. Default `true`.
- `verbose_faults` — whether verbose SOAP fault disclosure is checked. Default `true`.

---

## Identities

- `identities_ref` — a reference to two authorized controlled identities. It SHALL be
  a reference, never inline credentials.

---

## WSDL

- `wsdl_ref` — a reference to a discovered WSDL that enumerates operations and
  bindings.

---

## Limits

- `max_operations` — the maximum number of operations tested.
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

- `minimal_confirmation` — whether only minimal confirmation is recorded. Default
  `true` and SHALL NOT be disabled.
- `redact_sensitive` — whether sensitive content is redacted. Default `true` and SHALL
  NOT be disabled.

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
- `identities_ref` SHALL be a reference, never inline credentials.
- Numeric limits SHALL be positive.
- `max_requests_per_second` SHALL NOT exceed the policy ceiling.
- `minimal_confirmation` and `redact_sensitive` SHALL NOT be disabled.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
