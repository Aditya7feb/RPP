# Report Generation Configuration

**File:** `skills/reporting/report-generation/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Report Generation Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
report_generation:
  report_types:
    executive: true
    technical: true
  formats:
    enabled:
      - sarif
      - json
      - markdown
      - pdf
  templates:
    registry:
  presentation:
    distinguish_derived_risk: true
```

---

# Field Definitions

## report_types

`executive` and `technical` enable report audiences.

## formats

`enabled` enumerates the output serializations, produced through the shared Reporting package.
Formats are serializations, not capabilities.

## templates

`registry` enumerates the available report templates.

## presentation

`distinguish_derived_risk` SHALL default to `true`, requiring derived risk figures to be
distinguished from canonical Risk.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `report_type`, `formats`, and `template_ref`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `report_type` SHALL be `executive` or `technical`.
- `enabled` formats SHALL be supported by the shared Reporting package.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
