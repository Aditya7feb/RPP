# Finding Mapping Capabilities

**File:** `skills/reporting/finding-mapping/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Finding Mapping Capability. Each capability is
read-only over Findings and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| FM-1 | Finding loading | finding_refs | Loaded Findings |
| FM-2 | OWASP mapping | Findings | OWASP mappings |
| FM-3 | MITRE ATT&CK mapping | Findings | ATT&CK mappings |
| FM-4 | Mapping writing | mappings | Report content |
| FM-5 | Metrics emission | run | Metrics |

---

# FM-1 — Finding Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) by identifier without
modifying them.

---

# FM-2 — OWASP Mapping

The capability SHALL map Findings to OWASP categories for presentation, referencing existing Finding
classification such as CWE without altering it.

---

# FM-3 — MITRE ATT&CK Mapping

The capability SHALL map Findings to MITRE ATT&CK techniques for presentation.

---

# FM-4 — Mapping Writing

The capability SHALL produce mapping content for a [Report](../../../schemas/report.md) through the
shared [Reporting](../../shared/reporting/README.md) package.

---

# FM-5 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing mapping counts.

---

# Capability Boundaries

The capability SHALL NOT create, modify, or replace Findings, Risk, or Evidence, confirm
vulnerabilities, or classify Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface operations
in [interface.md](interface.md).
