# WebSocket API Security Skill Configuration

**File:** `skills/api-security/websocket/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the WebSocket API Security
Skill and the precedence rules that govern it. Configuration describes structure and
intent only.

---

# Configuration Object

```yaml
websocket_api_security:
  checks:
    origin_validation: true
    handshake_authentication: true
    message_authorization: true
    transport: true
    error_disclosure: true

  origin_validation:
    foreign_origin_probes:

  messages:
    max_messages:
    max_message_bytes:

  authorization:
    require_two_identities: true

  limits:
    max_actions:

  evidence:
    redact_sensitive: true
    capture_close_frames: true
```

---

# Field Definitions

## checks

Each boolean under `checks` enables or disables a capability. All checks default to
`true`.

## origin_validation

`foreign_origin_probes` bounds how many unexpected Origins the skill MAY present
during handshake evaluation. Probes SHALL originate only from controlled test values.

## messages

`max_messages` bounds the number of messages exchanged. `max_message_bytes` bounds
message size. These bounds SHALL prevent denial of service.

## authorization

`require_two_identities` requires two authorized controlled identities before message
authorization checks run. When identities are unavailable, those checks SHALL be
skipped and reported as not performed.

## limits

`max_actions` bounds the breadth of assessment. The skill SHALL NOT exceed this bound.

## evidence

`redact_sensitive` requires redaction of sensitive content. `capture_close_frames`
controls whether close-frame reasons are captured as evidence.

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

- `foreign_origin_probes`, `max_messages`, `max_message_bytes`, and `max_actions`
  SHALL be positive integers when present.
- `require_two_identities` SHOULD remain `true` for authorization checks.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
