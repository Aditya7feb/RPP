# Endpoint Enumeration Configuration

**File:** `skills/discovery/endpoint-enumeration/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Endpoint Enumeration
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
endpoint_enumeration:

  extraction:
    render_pages:
    extract_scripts:
    follow_inline_handlers:

  parameter_mining:
    enabled:
    max_parameters:
    wordlist_ref:

  limits:
    max_endpoints:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    capture_snippets:
    redact_secrets:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Extraction

- `render_pages` — whether rendered pages are analyzed. Default `true`.
- `extract_scripts` — whether client-side scripts are analyzed. Default `true`.
- `follow_inline_handlers` — whether inline event handlers are inspected. Default
  `true`.

---

## Parameter Mining

- `enabled` — whether parameter mining is performed. Default `false`.
- `max_parameters` — the maximum number of parameters to mine per endpoint.
- `wordlist_ref` — a reference to a managed parameter dictionary. It SHALL be a
  reference, never inline content.

---

## Limits

- `max_endpoints` — the maximum number of endpoints to enrich.
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

- `capture_snippets` — whether extraction snippets are captured. Default `true`.
- `redact_secrets` — whether client-side secrets are redacted in evidence per
  Rules of Engagement. Default `true`.

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
- Numeric limits SHALL be positive.
- `max_requests_per_second` SHALL NOT exceed the policy ceiling.
- `wordlist_ref` SHALL be a reference, never inline content.
- Unknown optional fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
