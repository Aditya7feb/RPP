# Risk Analysis Configuration

**File:** `skills/reporting/risk-analysis/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Risk Analysis Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
risk_analysis:
  functions:
    calculate_cvss: true
    normalize: true
    aggregate: true
    prioritize: true
    portfolio_metrics: true
  presentation:
    distinguish_derived: true
    canonical_authoritative: true
  bounds:
    max_findings:
```

---

# Field Definitions

## functions

Each boolean enables an analytical function. All default to `true`.

## presentation

`distinguish_derived` SHALL default to `true`, requiring derived values to be distinguished from
canonical Risk. `canonical_authoritative` SHALL default to `true` and SHALL NOT be disabled;
canonical Risk is always authoritative.

## bounds

`max_findings` bounds analysis scope. The capability SHALL NOT exceed this bound.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Canonical Risk authority (never overridden)
2. Per-request `analysis` and `bounds`
3. Capability configuration in this document
4. Documented defaults

---

# Validation Rules

- `canonical_authoritative` SHALL remain `true`.
- `max_findings` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
