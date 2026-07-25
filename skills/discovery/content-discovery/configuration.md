# Content Discovery Configuration

**File:** `skills/discovery/content-discovery/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Content Discovery Skill.

Configuration determines default wordlists, crawl and volume bounds,
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
content_discovery:

  wordlists:

  crawl:

  bounds:

  analysis:

  observability:
```

---

# Wordlists

```yaml
wordlists:
  default_ref:
  extensions:
```

`default_ref` SHALL reference the candidate-path list used when an invocation does
not specify one.

`extensions` SHALL enumerate file extensions appended to candidates, such as
`bak`, `old`, and `zip`.

---

# Crawl

```yaml
crawl:
  follow_links:
  max_depth:
  same_scope_only:
```

`follow_links` SHALL default to `true` within bounds.

`max_depth` SHALL bound crawl depth.

`same_scope_only` SHALL be `true`; only in-scope links SHALL be followed.

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
  detect_directory_listing:
  detect_backup_files:
  detect_admin_interfaces:
```

`detect_directory_listing`, `detect_backup_files`, and `detect_admin_interfaces`
SHALL toggle exposure analyses. Analyses SHALL produce Findings only with
supporting Evidence.

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

- `default_ref` references an existing wordlist
- `same_scope_only` is `true`
- `max_requests`, `max_concurrency`, `max_depth` are greater than or equal to `1`
- `per_request_timeout` is a positive duration
- `capture_evidence` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
content_discovery:

  wordlists:
    default_ref: wordlist-common-paths
    extensions:
      - bak
      - old
      - zip
      - tar.gz

  crawl:
    follow_links: true
    max_depth: 3
    same_scope_only: true

  bounds:
    max_requests: 10000
    max_concurrency: 16
    per_request_timeout: 8s

  analysis:
    detect_directory_listing: true
    detect_backup_files: true
    detect_admin_interfaces: true

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
