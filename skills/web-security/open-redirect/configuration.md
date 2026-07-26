# Open Redirect Configuration

**File:** `skills/web-security/open-redirect/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Open Redirect Skill and
the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
open_redirect:

  checks:
    parameter_controlled_redirect:
    untrusted_origin:
    weak_destination_validation:
    token_leakage:

  probing:
    probe_destination:
    candidate_parameters:

  limits:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    capture_redirect_target:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `parameter_controlled_redirect` — whether user-controllable redirect parameters
  are checked. Default `true`.
- `untrusted_origin` — whether redirection to an untrusted origin is checked.
  Default `true`.
- `weak_destination_validation` — whether substring, prefix, or suffix validation
  flaws are checked. Default `true`.
- `token_leakage` — whether sensitive-token leakage through the destination is
  checked. Default `true`.

---

## Probing

- `probe_destination` — a benign controlled destination used to confirm redirection.
  It SHALL NOT be a live malicious host.
- `candidate_parameters` — the parameters evaluated for redirect control.

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

- `capture_redirect_target` — whether the observed redirect target is captured in
  evidence, with sensitive tokens redacted. Default `true`.

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
- `probe_destination` SHALL be a benign controlled destination, never a live
  malicious host.
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
