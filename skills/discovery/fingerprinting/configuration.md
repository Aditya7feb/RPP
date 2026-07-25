# Fingerprinting Configuration

**File:** `skills/discovery/fingerprinting/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Fingerprinting Skill.

Configuration determines default signal sources, active-probing toggles, matching
and confidence thresholds, weakness-analysis toggles, and observability.

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

A higher-precedence source MAY tighten behavior but SHALL NOT bypass Policy
Engine gating.

---

# Configuration Structure

```yaml
fingerprinting:

  signals:

  matching:

  analysis:

  observability:
```

---

# Signals

```yaml
signals:
  default_sources:
  allow_active:
```

`default_sources` SHALL enumerate the signal sources consulted when an invocation
does not specify them, such as `headers`, `body`, `cookies`, `favicon`, and
`tls`.

`allow_active` SHALL be a boolean gating active probing and SHALL default to
`false`, preferring passive fingerprinting.

---

# Matching

```yaml
matching:
  min_confidence:
  version_inference:
```

`min_confidence` SHALL be the minimum confidence at which a Technology is
recorded.

`version_inference` SHALL be a boolean enabling version inference from signals;
inferred versions SHALL carry a lower confidence than observed versions.

---

# Analysis

```yaml
analysis:
  flag_outdated_versions:
  flag_version_disclosure:
```

`flag_outdated_versions` and `flag_version_disclosure` SHALL toggle
technology-exposure analyses. Analyses SHALL produce Findings only with supporting
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

- `default_sources` contains recognized signal sources
- `allow_active` defaults to `false`
- `min_confidence` is a valid confidence value
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
fingerprinting:

  signals:
    default_sources:
      - headers
      - body
      - cookies
      - favicon
      - tls
    allow_active: false

  matching:
    min_confidence: Medium
    version_inference: true

  analysis:
    flag_outdated_versions: true
    flag_version_disclosure: true

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Technology Schema](../../../schemas/technology.md)
- [Configuration Model](../../core/configuration-model.md)
