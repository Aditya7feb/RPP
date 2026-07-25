# Subdomain Discovery Configuration

**File:** `skills/discovery/subdomain-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Subdomain Discovery Skill.

Configuration determines passive sources, active-resolution toggles, candidate and
rate bounds, takeover-analysis toggles, and observability.

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
gating for active resolution.

---

# Configuration Structure

```yaml
subdomain_discovery:

  sources:

  bounds:

  analysis:

  observability:
```

---

# Sources

```yaml
sources:
  passive:
  active_resolution:
  wordlist_ref:
```

`passive` SHALL enumerate the passive sources consulted, such as
certificate-transparency and passive DNS references.

`active_resolution` SHALL be a boolean gating active resolution and SHALL default
to `true` subject to policy.

`wordlist_ref` SHALL reference the candidate list for active generation.

---

# Bounds

```yaml
bounds:
  max_candidates:
  max_concurrency:
  per_resolution_timeout:
```

`max_candidates` SHALL bound the number of candidates evaluated per invocation.

`max_concurrency` SHALL bound simultaneous resolutions.

`per_resolution_timeout` SHALL bound the time spent per resolution.

---

# Analysis

```yaml
analysis:
  detect_takeover:
  flag_internal_names:
```

`detect_takeover` SHALL toggle subdomain-takeover analysis from dangling
delegations and CNAMEs.

`flag_internal_names` SHALL toggle flagging of internal or staging names exposed
publicly.

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

- `wordlist_ref` references an existing wordlist when active resolution is enabled
- `max_candidates`, `max_concurrency` are greater than or equal to `1`
- `per_resolution_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
subdomain_discovery:

  sources:
    passive:
      - certificate-transparency
      - passive-dns
    active_resolution: true
    wordlist_ref: wordlist-subdomains

  bounds:
    max_candidates: 50000
    max_concurrency: 32
    per_resolution_timeout: 5s

  analysis:
    detect_takeover: true
    flag_internal_names: true

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
