# Workflow Runtime Configuration

**File:** `skills/shared/workflow-runtime/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Workflow Runtime Shared
Skill.

Configuration determines scheduling limits, approval enforcement, default
policies, state durability, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Workflow Runtime Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY tighten limits but SHALL NOT disable approval
enforcement.

---

# Configuration Structure

```yaml
workflow_runtime:

  scheduling:

  approvals:

  default_policies:

  state:

  observability:
```

---

# Scheduling

```yaml
scheduling:
  max_concurrency:
  step_timeout:
  workflow_timeout:
```

`max_concurrency` SHALL bound concurrent step dispatch.

`step_timeout` SHALL bound the duration of a single step.

`workflow_timeout` SHALL bound the total workflow duration.

---

# Approvals

```yaml
approvals:
  enforce:
  default_gate_on_intrusive:
```

`enforce` SHALL be a boolean and SHALL default to `true`. Approval enforcement
SHALL NOT be disabled through any configuration source.

`default_gate_on_intrusive` SHALL be a boolean requiring an approval gate before
any step classified as intrusive, even when a definition omits an explicit gate.

---

# Default Policies

```yaml
default_policies:
  rate_limit:
  retry:
  proxy:
```

`default_policies` SHALL reference canonical policy identifiers applied to steps
that do not specify their own.

Referenced policies SHALL exist and SHALL be valid.

---

# State

```yaml
state:
  durability:
  checkpoint_interval:
  resumable:
```

`durability` SHALL be one of `in_memory` or `durable`. `durable` SHALL be
required where resumption is needed.

`checkpoint_interval` SHALL bound how frequently state is persisted.

`resumable` SHALL be a boolean enabling resumption from durable state.

---

# Observability

```yaml
observability:
  emit_events:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `max_concurrency` is greater than or equal to `1`
- `approvals.enforce` is `true`
- Referenced default policies exist and are valid
- `state.durability` is one of the allowed values
- `resumable` implies `durability` is `durable`
- No secret material appears in configuration

---

# Example Configuration

```yaml
workflow_runtime:

  scheduling:
    max_concurrency: 8
    step_timeout: 120s
    workflow_timeout: 2h

  approvals:
    enforce: true
    default_gate_on_intrusive: true

  default_policies:
    rate_limit: ratelimitpolicy-default-http
    retry: retrypolicy-default-network
    proxy: proxy-corporate-egress

  state:
    durability: durable
    checkpoint_interval: 5s
    resumable: true

  observability:
    emit_events: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
- [Execution Plan Schema](../../../schemas/execution-plan.md)
- [Configuration Model](../../core/configuration-model.md)
