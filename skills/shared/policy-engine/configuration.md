# Policy Engine Configuration

**File:** `skills/shared/policy-engine/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Policy Engine Shared Skill.

Configuration determines default scope and Rules-of-Engagement references, the
default disposition, approval routing, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Policy Engine Shared Skill SHALL resolve configuration from the following
sources, in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY tighten authorization but SHALL NOT widen scope or
weaken a Rules-of-Engagement prohibition.

---

# Configuration Structure

```yaml
policy_engine:

  default_scope_id:

  default_roe_id:

  disposition:

  approval:

  observability:
```

---

# Default Policies

```yaml
default_scope_id:

default_roe_id:
```

`default_scope_id` SHALL reference the assessment
[Scope](../../../schemas/scope.md) applied when an invocation does not specify
one.

`default_roe_id` SHALL reference the assessment
[Rules of Engagement](../../../schemas/rules-of-engagement.md) applied when an
invocation does not specify one.

Both defaults SHALL exist and SHALL be valid.

---

# Disposition

```yaml
disposition:
  on_unknown_scope:
  fail_mode:
```

`on_unknown_scope` SHALL be one of `deny` or `require_approval` and SHALL default
to `deny`.

`fail_mode` SHALL be `fail_closed`. The Policy Engine SHALL NOT provide a
`fail_open` mode; an unresolved policy SHALL never yield an implicit allow.

---

# Approval

```yaml
approval:
  route:
  cache_grants:
```

`route` SHALL identify how `requires_approval` decisions are routed to the master
agent approval process, expressed abstractly.

`cache_grants` SHALL be a boolean. When `true`, a granted approval MAY authorize
subsequent identical actions within its validity, subject to Rules of Engagement.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of decision events.

`capture_evidence` SHALL enable decision-record evidence conforming to the
[Evidence schema](../../../schemas/evidence.md) and SHALL default to `true`.

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `default_scope_id` references an existing Scope
- `default_roe_id` references an existing Rules of Engagement
- `on_unknown_scope` is `deny` or `require_approval`
- `fail_mode` is `fail_closed`
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
policy_engine:

  default_scope_id: scope-asmt-42

  default_roe_id: roe-asmt-42

  disposition:
    on_unknown_scope: deny
    fail_mode: fail_closed

  approval:
    route: master-agent-approval
    cache_grants: true

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
- [Configuration Model](../../core/configuration-model.md)
