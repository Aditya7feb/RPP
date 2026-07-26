# Report Generation Interface

**File:** `skills/reporting/report-generation/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Report Generation
Capability.

---

# Operation: generate

## Request

```yaml
generate:
  report_type:
  finding_refs:
  risk_refs:
  evidence_refs:
  content:
    correlation_ref:
    analysis_ref:
    mapping_ref:
  formats:
  template_ref:
```

`report_type` selects `executive` or `technical`. `content` references reporting content. `formats`
selects output serializations. `template_ref` references a template.

## Response

```yaml
generate_result:
  report_ref:
  serialized_outputs:
    - format:
      artifact_ref:
  metrics_ref:
```

`report_ref` references a generated [Report](../../../schemas/report.md); `serialized_outputs`
reference the produced serializations; `metrics_ref` references
[Metrics](../../../schemas/metrics.md). Outputs reference canonical objects by identifier and contain
no new Findings or Risk.

---

# Preconditions

- Referenced canonical objects SHALL exist.
- `report_type` SHALL be `executive` or `technical`.

---

# Postconditions

- Canonical objects SHALL NOT have been modified.
- Formats SHALL have been produced as serializations of the Report.
- No new Findings or Risk SHALL be produced.

---

# Error Semantics

Error categories are defined in [error-model.md](error-model.md).

---

# Interface Stability

The `generate` operation is stable. Additional report types and formats MAY be introduced in a
backward-compatible manner. Consumers SHALL ignore unknown response fields.

---

# Related Documents

- [capabilities.md](capabilities.md)
- [configuration.md](configuration.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
