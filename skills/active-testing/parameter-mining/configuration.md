# Parameter Mining Configuration

**File:** `skills/active-testing/parameter-mining/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Parameter Mining Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
parameter_mining:
  locations:
    enabled:
  candidate_source:
    default_wordlist:
    default_max_candidates:
  bounds:
    max_requests:
    batch_size:
  detection:
    reflection: true
    behavior_change: true
  evidence:
    capture_interactions: true
```

---

# Field Definitions

## locations

`enabled` enumerates the probe locations (query, body, header, cookie).

## candidate_source

`default_wordlist` and `default_max_candidates` bound candidate sourcing.

## bounds

`max_requests` and `batch_size` bound request volume. The capability SHALL NOT exceed these
bounds.

## detection

`reflection` and `behavior_change` enable detection modes.

## evidence

`capture_interactions` controls whether probe interactions are captured as Artifacts.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-request parameters
4. Capability configuration in this document
5. Documented defaults

Policy Engine decisions SHALL always override requested parameters.

---

# Validation Rules

- `max_requests`, `batch_size`, and `default_max_candidates` SHALL be positive integers when
  present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
