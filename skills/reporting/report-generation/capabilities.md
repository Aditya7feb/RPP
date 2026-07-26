# Report Generation Capabilities

**File:** `skills/reporting/report-generation/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Report Generation Capability. Each capability is
read-only over canonical objects and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| RG-1 | Input loading | refs, content | Loaded inputs |
| RG-2 | Executive composition | inputs | Executive report |
| RG-3 | Technical composition | inputs | Technical report |
| RG-4 | Serialization | report, formats | Serialized outputs |
| RG-5 | Report writing | report | Report |
| RG-6 | Metrics emission | run | Metrics |

---

# RG-1 — Input Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md),
[Risk](../../../schemas/risk.md), [Evidence](../../../schemas/evidence.md), and correlation,
analysis, and mapping content by identifier without modifying them.

---

# RG-2 — Executive Composition

The capability SHALL compose an executive report for stakeholder audiences.

---

# RG-3 — Technical Composition

The capability SHALL compose a technical report for practitioner audiences.

---

# RG-4 — Serialization

The capability SHALL serialize a [Report](../../../schemas/report.md) to SARIF, JSON, Markdown, and
PDF through the shared [Reporting](../../shared/reporting/README.md) package. Formats are
serializations, not capabilities.

---

# RG-5 — Report Writing

The capability SHALL produce a [Report](../../../schemas/report.md) referencing canonical objects by
identifier.

---

# RG-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing generation.

---

# Capability Boundaries

The capability SHALL NOT create, modify, or replace Findings, Risk, or Evidence, own canonical Risk,
or treat output formats as distinct capabilities.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface operations
in [interface.md](interface.md).
