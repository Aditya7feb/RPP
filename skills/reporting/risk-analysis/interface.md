# Risk Analysis Interface

**File:** `skills/reporting/risk-analysis/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Risk Analysis
Capability.

---

# Operation: analyze

## Request

```yaml
analyze:
  finding_refs:
  risk_refs:
  analysis:
    calculate_cvss:
    normalize:
    aggregate:
    prioritize:
    portfolio_metrics:
  bounds:
    max_findings:
```

`finding_refs` and `risk_refs` reference inputs. `analysis` selects functions. `bounds` limits scope.

## Response

```yaml
analyze_result:
  analysis_ref:
  derived_cvss:
  normalized_scores:
  aggregate_risk:
  prioritized_findings:
  portfolio_metrics:
  metrics_ref:
```

`analysis_ref` references analysis content for a [Report](../../../schemas/report.md). All scoring
fields are **derived, presentation-only** figures; canonical [Risk](../../../schemas/risk.md) remains
authoritative. `metrics_ref` references [Metrics](../../../schemas/metrics.md).

---

# Preconditions

- `finding_refs` and `risk_refs` SHALL reference existing canonical objects.
- `max_findings` SHALL be a positive integer when present.

---

# Postconditions

- Canonical Findings and Risk SHALL NOT have been modified.
- Derived values SHALL be distinguished from canonical Risk.
- No new Findings or canonical Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `analyze` operation is stable. Additional analytical functions MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
