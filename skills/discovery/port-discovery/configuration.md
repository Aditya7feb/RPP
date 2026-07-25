# Port Discovery Configuration

**File:** `skills/discovery/port-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Port Discovery Skill.

Configuration determines default port sets, protocols, timing and volume bounds,
weakness-analysis toggles, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The skill SHALL resolve configuration from the following sources, in increasing
order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY tighten bounds but SHALL NOT bypass Policy Engine
gating or the rate ceiling.

---

# Configuration Structure

```yaml
port_discovery:

  ports:

  protocols:

  bounds:

  analysis:

  observability:
```

---

# Ports

```yaml
ports:
  default_set:
```

`default_set` SHALL declare the ports probed when an invocation does not specify
them, such as a curated common-services set.

Unbounded full-range probing SHALL require explicit configuration and remains
subject to the policy rate ceiling.

---

# Protocols

```yaml
protocols:
  default:
```

`default` SHALL be one of `tcp`, `udp`, or `both`.

---

# Bounds

```yaml
bounds:
  max_ports:
  max_concurrency:
  per_port_timeout:
```

`max_ports` SHALL bound the number of ports probed per invocation.

`max_concurrency` SHALL bound simultaneous probes.

`per_port_timeout` SHALL bound the time spent per port.

---

# Analysis

```yaml
analysis:
  flag_admin_services:
  flag_plaintext_services:
  baseline_ref:
```

`flag_admin_services` and `flag_plaintext_services` SHALL toggle exposure
analyses.

`baseline_ref` MAY reference an expected-service baseline; services outside the
baseline MAY be flagged. Analyses SHALL produce Findings only with supporting
Evidence.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md) and SHALL default to `true`.

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `default` protocol is `tcp`, `udp`, or `both`
- `max_ports`, `max_concurrency` are greater than or equal to `1`
- `per_port_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
port_discovery:

  ports:
    default_set: common-services

  protocols:
    default: tcp

  bounds:
    max_ports: 1024
    max_concurrency: 64
    per_port_timeout: 3s

  analysis:
    flag_admin_services: true
    flag_plaintext_services: true
    baseline_ref: baseline-asmt-42

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
