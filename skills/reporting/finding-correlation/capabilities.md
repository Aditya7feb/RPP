# Finding Correlation Capabilities

**File:** `skills/reporting/finding-correlation/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities of the Finding Correlation Capability. Each capability is
read-only over Findings and produces no Findings or Risk.

---

# Capability Summary

| ID | Capability | Input | Output |
|----|------------|-------|--------|
| FC-1 | Finding loading | finding_refs | Loaded Findings |
| FC-2 | Deduplication | Findings | Deduplicated groups |
| FC-3 | Relation | Findings | Related-finding links |
| FC-4 | Attack-chain construction | Findings | Attack chains |
| FC-5 | Correlation writing | correlation | Report content |
| FC-6 | Metrics emission | run | Metrics |

---

# FC-1 — Finding Loading

The capability SHALL load referenced [Findings](../../../schemas/finding.md) by identifier without
modifying them.

---

# FC-2 — Deduplication

The capability SHALL group Findings that describe the same underlying issue, referencing them by
identifier.

---

# FC-3 — Relation

The capability SHALL relate Findings that share a target, root cause, or attack path.

---

# FC-4 — Attack-Chain Construction

The capability SHALL construct attack chains from related Findings, preserving ordering.

---

# FC-5 — Correlation Writing

The capability SHALL produce correlation content for a [Report](../../../schemas/report.md) through
the shared [Reporting](../../shared/reporting/README.md) package.

---

# FC-6 — Metrics Emission

The capability SHALL emit [Metrics](../../../schemas/metrics.md) describing correlation counts.

---

# Capability Boundaries

The capability SHALL NOT create, modify, or replace Findings, Risk, or Evidence, confirm
vulnerabilities, or classify Risk.

---

# Traceability

Each capability maps to execution stages in [execution.md](execution.md) and to interface operations
in [interface.md](interface.md).
