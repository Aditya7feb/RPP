# gRPC API Security Skill Configuration

**File:** `skills/api-security/grpc/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the gRPC API Security Skill
and the precedence rules that govern it. Configuration describes structure and intent
only.

---

# Configuration Object

```yaml
grpc_api_security:
  checks:
    reflection: true
    transport: true
    method_authorization: true
    object_authorization: true
    resource_consumption: true
    status_disclosure: true

  resource_consumption:
    max_message_probe_bytes:
    max_stream_messages:
    incremental: true

  authorization:
    require_two_identities: true

  limits:
    max_methods:
    max_actions:

  evidence:
    redact_sensitive: true
    capture_status_detail: true
```

---

# Field Definitions

## checks

Each boolean under `checks` enables or disables a capability. All checks default to
`true`.

## resource_consumption

`max_message_probe_bytes` bounds the largest message the skill MAY send. `max_stream_messages`
bounds streaming probes. `incremental` requires probes to grow in bounded steps rather
than jumping to a maximum. These bounds SHALL prevent denial of service.

## authorization

`require_two_identities` requires two authorized controlled identities before
authorization checks run. When identities are unavailable, authorization checks SHALL
be skipped and reported as not performed.

## limits

`max_methods` and `max_actions` bound the breadth of assessment. The skill SHALL NOT
exceed these bounds.

## evidence

`redact_sensitive` requires redaction of sensitive content. `capture_status_detail`
controls whether gRPC status detail is captured as evidence.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-assessment `options` in the `assess` request
4. Skill configuration in this document
5. Documented defaults

Rules of Engagement and Policy Engine decisions SHALL always override requested
options. A more permissive configuration SHALL NOT override a more restrictive policy
decision.

---

# Validation Rules

- `max_message_probe_bytes`, `max_stream_messages`, `max_methods`, and `max_actions`
  SHALL be positive integers when present.
- `require_two_identities` SHOULD remain `true` for authorization checks.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
