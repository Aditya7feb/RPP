# TLS Analysis Configuration

**File:** `skills/discovery/tls-analysis/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the TLS Analysis Skill.

Configuration determines default checks, weakness thresholds, interception
handling, and observability.

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

A higher-precedence source MAY tighten thresholds but SHALL NOT bypass Policy
Engine gating.

---

# Configuration Structure

```yaml
tls_analysis:

  checks:

  thresholds:

  interception:

  observability:
```

---

# Checks

```yaml
checks:
  default:
```

`default` SHALL enumerate the analyses performed when an invocation does not
specify them, such as `protocols`, `ciphers`, `certificate`, and `validation`.

---

# Thresholds

```yaml
thresholds:
  min_protocol:
  weak_ciphers:
  cert_expiry_warning:
```

`min_protocol` SHALL declare the minimum acceptable protocol version; offering a
lower version MAY be flagged.

`weak_ciphers` SHALL enumerate cipher classes considered weak.

`cert_expiry_warning` SHALL be a duration within which impending expiry is
flagged.

Thresholds inform analysis; Findings SHALL be produced only with supporting
Evidence.

---

# Interception

```yaml
interception:
  honor_boundaries:
```

`honor_boundaries` SHALL be a boolean and SHALL default to `true`. When `true`,
interception boundaries reported by the
[TLS Client](../../shared/tls-client/README.md) SHALL NOT be reported as
certificate weaknesses.

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

- `checks.default` contains recognized analyses
- `min_protocol` is a recognized protocol version
- `cert_expiry_warning` is a positive duration
- `honor_boundaries` is `true`
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
tls_analysis:

  checks:
    default:
      - protocols
      - ciphers
      - certificate
      - validation

  thresholds:
    min_protocol: TLS1.2
    weak_ciphers:
      - export
      - null
      - rc4
    cert_expiry_warning: 30d

  interception:
    honor_boundaries: true

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
