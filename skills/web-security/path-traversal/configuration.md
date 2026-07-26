# Path Traversal Configuration

**File:** `skills/web-security/path-traversal/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Path Traversal Skill and
the precedence rules that resolve it. Configuration is data; it never contains
implementation logic.

---

# Configuration Object

```yaml
path_traversal:

  checks:
    traversal_sequences:
    encoding_bypass:
    canonicalization:

  probing:
    marker_ref:
    candidate_parameters:
    max_depth:

  limits:
    max_parameters:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_marker_read:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `traversal_sequences` — whether traversal sequences are checked. Default `true`.
- `encoding_bypass` — whether encoded and double-encoded traversal is checked.
  Default `true`.
- `canonicalization` — whether canonicalization adequacy is assessed. Default
  `true`.

---

## Probing

- `marker_ref` — a reference to a non-sensitive marker resource used to confirm
  traversal. It SHALL NOT reference a sensitive file.
- `candidate_parameters` — the parameters evaluated for path control.
- `max_depth` — the maximum traversal depth attempted.

---

## Limits

- `max_parameters` — the maximum number of path parameters tested.
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

- `record_marker_read` — whether the non-sensitive marker read is recorded in
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
- `max_depth` and numeric limits SHALL be positive.
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
