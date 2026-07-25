# API Discovery Configuration

**File:** `skills/discovery/api-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the API Discovery Skill.

Configuration determines default specification hints, GraphQL detection, base-path
candidates, volume and rate bounds, weakness-analysis toggles, and observability.

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
api_discovery:

  definitions:

  graphql:

  base_paths:

  bounds:

  analysis:

  observability:
```

---

# Definitions

```yaml
definitions:
  default_hints:
```

`default_hints` SHALL enumerate candidate specification paths consulted when an
invocation does not specify them, such as `/openapi.json`, `/swagger.json`, and
`/api-docs`.

---

# GraphQL

```yaml
graphql:
  detect:
  test_introspection:
```

`detect` SHALL be a boolean enabling GraphQL endpoint detection.

`test_introspection` SHALL be a boolean enabling an introspection query; the query
SHALL be gated by the Policy Engine as an active action.

---

# Base Paths

```yaml
base_paths:
  candidates_ref:
```

`candidates_ref` SHALL reference the candidate API base-path list, such as
`/api`, `/v1`, and `/graphql`.

---

# Bounds

```yaml
bounds:
  max_requests:
  max_concurrency:
  per_request_timeout:
```

`max_requests` SHALL bound the number of requests per invocation.

`max_concurrency` SHALL bound simultaneous requests.

`per_request_timeout` SHALL bound the time spent per request.

---

# Analysis

```yaml
analysis:
  flag_public_specifications:
  flag_introspection_enabled:
  flag_debug_endpoints:
```

`flag_public_specifications`, `flag_introspection_enabled`, and
`flag_debug_endpoints` SHALL toggle API-exposure analyses. Analyses SHALL produce
Findings only with supporting Evidence.

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

- `default_hints` contains recognized specification paths
- `candidates_ref` references an existing base-path list
- `max_requests`, `max_concurrency` are greater than or equal to `1`
- `per_request_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
api_discovery:

  definitions:
    default_hints:
      - /openapi.json
      - /swagger.json
      - /api-docs
      - /.well-known/openapi

  graphql:
    detect: true
    test_introspection: true

  base_paths:
    candidates_ref: wordlist-api-paths

  bounds:
    max_requests: 2000
    max_concurrency: 16
    per_request_timeout: 8s

  analysis:
    flag_public_specifications: true
    flag_introspection_enabled: true
    flag_debug_endpoints: true

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
