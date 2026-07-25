# DNS Enumeration Configuration

**File:** `skills/discovery/dns-enumeration/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the DNS Enumeration Skill.

Configuration determines default record types, recursion and volume bounds,
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
gating or scope enforcement.

---

# Configuration Structure

```yaml
dns_enumeration:

  records:

  bounds:

  analysis:

  observability:
```

---

# Records

```yaml
records:
  default_types:
```

`default_types` SHALL enumerate the record classes queried when an invocation
does not specify them, such as `A`, `AAAA`, `CNAME`, `MX`, `NS`, `TXT`, `SOA`,
and `SRV`.

---

# Bounds

```yaml
bounds:
  max_names:
  max_depth:
  per_name_timeout:
```

`max_names` SHALL bound the number of names enumerated per invocation.

`max_depth` SHALL bound recursive enumeration depth.

`per_name_timeout` SHALL bound the time spent per name.

---

# Analysis

```yaml
analysis:
  detect_zone_transfer:
  detect_dangling_records:
  detect_wildcards:
```

`detect_zone_transfer`, `detect_dangling_records`, and `detect_wildcards` SHALL
toggle weakness analyses. Analyses SHALL produce Findings only with supporting
Evidence.

Zone-transfer testing SHALL be treated as an `active` action and gated by the
Policy Engine.

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

- `default_types` contains recognized DNS record classes
- `max_names`, `max_depth` are greater than or equal to `1`
- `per_name_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
dns_enumeration:

  records:
    default_types:
      - A
      - AAAA
      - CNAME
      - MX
      - NS
      - TXT
      - SOA
      - SRV

  bounds:
    max_names: 5000
    max_depth: 2
    per_name_timeout: 5s

  analysis:
    detect_zone_transfer: true
    detect_dangling_records: true
    detect_wildcards: true

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
