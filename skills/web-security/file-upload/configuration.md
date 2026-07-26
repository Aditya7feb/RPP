# Unrestricted File Upload Configuration

**File:** `skills/web-security/file-upload/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Unrestricted File Upload
Skill and the precedence rules that resolve it. Configuration is data; it never
contains implementation logic.

---

# Configuration Object

```yaml
file_upload:

  checks:
    type_validation:
    content_validation:
    storage_exposure:
    executable_content_type:

  markers:
    marker_set_ref:
    max_markers_per_endpoint:

  limits:
    max_endpoints:
    max_requests:
    request_timeout_ms:

  rate:
    respect_policy_ceiling:
    max_requests_per_second:

  evidence:
    record_upload:
    redact_sensitive:

  policy:
    scope_id:
    roe_id:
```

---

# Field Definitions

## Checks

- `type_validation` — whether file-type validation adequacy is checked. Default
  `true`.
- `content_validation` — whether content validation beyond declared type is checked.
  Default `true`.
- `storage_exposure` — whether web-accessible storage is checked. Default `true`.
- `executable_content_type` — whether uploaded content is served with an executable
  or unsafe content type. Default `true`.

---

## Markers

- `marker_set_ref` — a reference to a managed set of inert, non-executable marker
  files. It SHALL be a reference, never functional malicious payloads.
- `max_markers_per_endpoint` — the maximum number of markers tried per endpoint.

---

## Limits

- `max_endpoints` — the maximum number of upload endpoints tested.
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

- `record_upload` — whether the inert marker upload is recorded in evidence. Default
  `true`.
- `redact_sensitive` — whether sensitive content is redacted. Default `true`.

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
- `marker_set_ref` SHALL be a reference to inert markers, never functional malicious
  payloads.
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
