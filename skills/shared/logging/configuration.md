# Logging Configuration

**File:** `skills/shared/logging/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Logging Shared Skill.

Configuration determines severity thresholds, category enablement, redaction
rules, sink routing, and failure behavior.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Logging Shared Skill SHALL resolve configuration from the following sources,
in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY raise verbosity but SHALL NOT disable redaction.

---

# Configuration Structure

```yaml
logging:

  level:

  categories:

  redaction:

  sinks:

  failure_mode:
```

---

# Level

```yaml
level:
```

`level` SHALL be the minimum severity emitted and SHALL be one of the severities
defined in the [Log Event schema](../../../schemas/log-event.md).

Events below `level` SHALL be dropped.

---

# Categories

```yaml
categories:
  enabled:
  disabled:
```

`enabled` SHALL list categories that are emitted.

`disabled` SHALL list categories that are suppressed.

`security_event` and `audit` categories SHALL NOT be disabled, preserving the
audit trail.

---

# Redaction

```yaml
redaction:
  enabled:
  patterns:
  fields:
```

`enabled` SHALL be a boolean and SHALL default to `true`. Redaction SHALL NOT be
disabled through any configuration source.

`patterns` SHALL describe value patterns treated as secrets.

`fields` SHALL list attribute keys always redacted, such as `authorization` and
`set-cookie`.

---

# Sinks

```yaml
sinks:
  - name:
    kind:
    min_level:
    categories:
```

`sinks` SHALL enumerate configured destinations.

`kind` SHALL identify an adapter kind without exposing implementation details.

`min_level` SHALL bound the severity routed to the sink.

`categories` SHALL bound the categories routed to the sink.

---

# Failure Mode

```yaml
failure_mode:
```

`failure_mode` SHALL be one of

```
fail_open

fail_closed
```

`fail_open` SHALL allow the caller operation to proceed when a sink fails.

`fail_closed` SHALL propagate a logging error when a required sink fails and is
appropriate only for audit-critical contexts.

The default SHALL be `fail_open`.

---

# Resolution Order

The Logging Shared Skill SHALL resolve settings as follows.

```
Invocation Override

↓ (if absent)

Consumer Configuration

↓ (if absent)

Assessment Configuration

↓ (if absent)

Platform Defaults

↓

Enforce Mandatory Redaction
```

---

# Validation Rules

A valid configuration SHALL satisfy

- `level` is a valid severity
- `security_event` and `audit` are not in `categories.disabled`
- `redaction.enabled` is `true`
- Every sink defines a `kind`
- `failure_mode` is one of the allowed values
- No secret material appears in configuration

---

# Example Configuration

```yaml
logging:

  level: info

  categories:
    enabled:
      - lifecycle
      - execution
      - network
      - security_event
      - audit
    disabled:
      - diagnostic

  redaction:
    enabled: true
    fields:
      - authorization
      - set-cookie
      - proxy-authorization
    patterns:
      - bearer-token
      - api-key

  sinks:
    - name: primary
      kind: stream
      min_level: info
      categories:
        - lifecycle
        - execution
        - network
    - name: audit
      kind: audit-store
      min_level: info
      categories:
        - security_event
        - audit

  failure_mode: fail_open
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Log Event Schema](../../../schemas/log-event.md)
- [Configuration Model](../../core/configuration-model.md)
