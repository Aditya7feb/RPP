# SSH Client Configuration

**File:** `skills/shared/ssh-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the SSH Client Shared Skill.

Configuration determines host-key trust defaults, authentication-attempt bounds,
execution gating, output and session bounds, governance policy defaults, and
observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The SSH Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY strengthen trust or tighten bounds but SHALL NOT
weaken a `strict` host-key policy where mandated.

---

# Configuration Structure

```yaml
ssh_client:

  host_key:

  authentication:

  execution:

  bounds:

  governance:

  observability:
```

---

# Host Key

```yaml
host_key:
  default_trust_policy:
  known_host_ref:
```

`default_trust_policy` SHALL be one of `strict`, `trust_on_first_use`, or
`record_only`.

`record_only` SHALL be permitted only for explicitly scoped discovery contexts.

`known_host_ref` SHALL reference the known-host store.

---

# Authentication

```yaml
authentication:
  max_attempts:
  allowed_methods:
```

`max_attempts` SHALL bound authentication attempts to prevent brute-force
behavior.

`allowed_methods` SHALL enumerate permitted authentication methods.

---

# Execution

```yaml
execution:
  allow_command_execution:
  allow_shell:
  allow_forwarding:
```

`allow_command_execution` and `allow_shell` SHALL gate intrusive execution.

`allow_forwarding` SHALL gate port forwarding.

All SHALL default to `false` and be enabled only where authorized.

---

# Bounds

```yaml
bounds:
  max_output_bytes:
  session_timeout:
  command_timeout:
```

`max_output_bytes` SHALL bound command output.

`session_timeout` and `command_timeout` SHALL bound session and command
durations.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own. The proxy MAY provide jump-host traversal.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable session evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `default_trust_policy` is one of the allowed policies
- `max_attempts` is greater than or equal to `1`
- `allow_command_execution`, `allow_shell`, and `allow_forwarding` default to
  `false`
- `max_output_bytes` is greater than or equal to `1`
- `session_timeout` and `command_timeout` are positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
ssh_client:

  host_key:
    default_trust_policy: strict
    known_host_ref: knownhosts-asmt-42

  authentication:
    max_attempts: 3
    allowed_methods:
      - public_key
      - password

  execution:
    allow_command_execution: false
    allow_shell: false
    allow_forwarding: false

  bounds:
    max_output_bytes: 2MB
    session_timeout: 120s
    command_timeout: 30s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Configuration Model](../../core/configuration-model.md)
