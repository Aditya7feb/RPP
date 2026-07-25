# Reporting Configuration

**File:** `skills/shared/reporting/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Reporting Shared Skill.

Configuration determines composition defaults, deduplication and correlation
behavior, ordering, evidence bundling, renderers, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Reporting Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY change composition behavior but SHALL NOT disable
redaction preservation in evidence bundles.

---

# Configuration Structure

```yaml
reporting:

  composition:

  ordering:

  evidence:

  renderers:

  observability:
```

---

# Composition

```yaml
composition:
  deduplicate:
  correlate:
  merge_evidence_on_dedup:
```

`deduplicate` SHALL enable deduplication by default.

`correlate` SHALL enable correlation by default.

`merge_evidence_on_dedup` SHALL be `true`, ensuring deduplication merges rather
than discards evidence references.

---

# Ordering

```yaml
ordering:
  order_by:
  tie_breaker:
```

`order_by` SHALL be one of `severity`, `confidence`, or
`severity_then_confidence`.

`tie_breaker` SHALL define a stable secondary ordering, such as `finding_id`, to
ensure deterministic output.

---

# Evidence

```yaml
evidence:
  include_by_default:
  preserve_redaction:
  bundle_scope:
```

`include_by_default` SHALL determine whether evidence is bundled unless overridden.

`preserve_redaction` SHALL be `true` and SHALL NOT be disabled, ensuring rendered
output never exposes redacted material.

`bundle_scope` SHALL bound which evidence scopes MAY be bundled into a report.

---

# Renderers

```yaml
renderers:
  - format:
    kind:
    enabled:
```

`renderers` SHALL enumerate configured output renderers.

`format` SHALL identify the output format, such as `json`, `sarif`, `markdown`,
or `pdf`.

`kind` SHALL identify an adapter kind without exposing implementation details.

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

- `order_by` is one of the allowed values
- `tie_breaker` is defined for deterministic ordering
- `merge_evidence_on_dedup` is `true`
- `preserve_redaction` is `true`
- Every renderer defines a `format` and `kind`
- No secret material appears in configuration

---

# Example Configuration

```yaml
reporting:

  composition:
    deduplicate: true
    correlate: true
    merge_evidence_on_dedup: true

  ordering:
    order_by: severity_then_confidence
    tie_breaker: finding_id

  evidence:
    include_by_default: true
    preserve_redaction: true
    bundle_scope: assessment

  renderers:
    - format: json
      kind: structured
      enabled: true
    - format: sarif
      kind: structured
      enabled: true
    - format: markdown
      kind: document
      enabled: true
    - format: pdf
      kind: document
      enabled: false

  observability:
    emit_events: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Report Schema](../../../schemas/report.md)
- [Configuration Model](../../core/configuration-model.md)
