# Virtual Host Discovery Configuration

**File:** `skills/discovery/virtual-host-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Virtual Host Discovery
Skill.

Configuration determines candidate sources, differential thresholds, volume and
rate bounds, weakness-analysis toggles, and observability.

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
virtual_host_discovery:

  candidates:

  differential:

  bounds:

  analysis:

  observability:
```

---

# Candidates

```yaml
candidates:
  default_ref:
  include_discovered_subdomains:
```

`default_ref` SHALL reference the candidate host-name list used when an invocation
does not specify one.

`include_discovered_subdomains` SHALL be a boolean including previously discovered
subdomains as candidates.

---

# Differential

```yaml
differential:
  similarity_threshold:
  detect_wildcard:
```

`similarity_threshold` SHALL define how different a candidate response must be from
the baseline to be considered a distinct virtual host.

`detect_wildcard` SHALL be a boolean enabling wildcard-response detection to reduce
false positives.

---

# Bounds

```yaml
bounds:
  max_candidates:
  max_concurrency:
  per_request_timeout:
```

`max_candidates` SHALL bound the number of candidates probed per invocation.

`max_concurrency` SHALL bound simultaneous probes.

`per_request_timeout` SHALL bound the time spent per probe.

---

# Analysis

```yaml
analysis:
  flag_internal_hosts:
  flag_staging_hosts:
```

`flag_internal_hosts` and `flag_staging_hosts` SHALL toggle hidden-host analyses.
Analyses SHALL produce Findings only with supporting Evidence.

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

- `default_ref` references an existing candidate list
- `similarity_threshold` is a valid proportion
- `max_candidates`, `max_concurrency` are greater than or equal to `1`
- `per_request_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
virtual_host_discovery:

  candidates:
    default_ref: wordlist-vhosts
    include_discovered_subdomains: true

  differential:
    similarity_threshold: 0.85
    detect_wildcard: true

  bounds:
    max_candidates: 20000
    max_concurrency: 16
    per_request_timeout: 8s

  analysis:
    flag_internal_hosts: true
    flag_staging_hosts: true

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
