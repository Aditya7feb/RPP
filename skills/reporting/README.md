# Reporting Capability Tier

**File:** `skills/reporting/README.md`

**Version:** 1.0.0

---

# Purpose

The Reporting tier provides reusable, implementation-independent capabilities that **consume**
Findings, Risk, and Evidence and produce reports within the Robust PenTest Platform (RPP).

Reporting capabilities correlate, analyze, map, generate, and bundle for presentation. They are
**read-only** over their inputs: Findings, canonical Risk, and Evidence are immutable and are never
created, modified, or replaced by Reporting.

This tier comprises the following capabilities.

- [Finding Correlation](finding-correlation/README.md)
- [Risk Analysis](risk-analysis/README.md)
- [Finding Mapping](finding-mapping/README.md)
- [Report Generation](report-generation/README.md)
- [Evidence Bundle](evidence-bundle/README.md)

---

# Ownership Boundary

Ownership of canonical objects is fixed and Reporting does not hold it.

| Owner | Owns |
|-------|------|
| Domain Security | confirms vulnerabilities, produces Findings, produces canonical Risk |
| Reporting tier | consumes Findings, Risk, and Evidence; correlates, analyzes, maps, generates, and bundles for presentation |
| Shared `reporting` | rendering and serialization primitives (SARIF, JSON, Markdown, PDF), templating |
| Evidence tier / shared `evidence` | evidence collection and durable lifecycle |

Reporting SHALL NOT

- create, modify, or replace canonical [Risk](../../schemas/risk.md)
- modify [Findings](../../schemas/finding.md) or [Evidence](../../schemas/evidence.md)
- capture evidence or confirm vulnerabilities

## Canonical Risk Authority

Domain Security owns canonical [Risk](../../schemas/risk.md). Reporting MAY calculate CVSS vectors
for presentation, normalize scores, aggregate risk, prioritize findings, compute portfolio-level
metrics, and generate executive summaries. These are **presentation and analytical functions**;
they SHALL NOT replace or mutate canonical Risk. **Where a calculated value differs from the
canonical Risk, the canonical Risk remains authoritative**, and the calculated value SHALL be
presented as a derived, presentation-only figure.

---

# Immutability

Findings, Risk, and Evidence are immutable inputs to Reporting. Reporting capabilities SHALL
reference these canonical objects by identifier and SHALL NOT alter them. Derived values produced
for presentation SHALL be clearly distinguished from the canonical objects they are derived from.

---

# Output Formats

Report output formats — SARIF, JSON, Markdown, and PDF — are **serializations, not capabilities**.
They are produced by [Report Generation](report-generation/README.md) through the shared
[Reporting](../shared/reporting/README.md) package. No format is a separate capability package.

---

# Capability Responsibilities

| Capability | Responsibility |
|------------|----------------|
| Finding Correlation | deduplicate, relate, and chain Findings |
| Risk Analysis | CVSS calculation, normalization, aggregation, prioritization, portfolio metrics (presentation only) |
| Finding Mapping | OWASP and MITRE ATT&CK mapping enrichment for presentation |
| Report Generation | executive and technical reports serialized to SARIF, JSON, Markdown, and PDF |
| Evidence Bundle | assemble referenced Evidence into a distributable bundle |

---

# Data Flow

```
Domain Security                Reporting tier                       Consumers
───────────────                ──────────────                       ─────────
Findings · Risk · Evidence ──► correlate · analyze · map ·      ──► stakeholders
(immutable, canonical)         generate · bundle (read-only)        (reports, bundles)
```

Reporting consumes canonical Findings, Risk, and Evidence and produces reports and bundles. It
never mutates its inputs and never owns canonical Risk.

---

# Canonical Schemas

- [Report](../../schemas/report.md)
- [Finding](../../schemas/finding.md)
- [Risk](../../schemas/risk.md)
- [Evidence](../../schemas/evidence.md)
- [Metrics](../../schemas/metrics.md)

The Reporting tier introduces no new canonical schemas.

---

# Related

- [Shared Infrastructure](../shared/README.md)
- [Reporting (shared)](../shared/reporting/README.md)
- [Evidence (shared)](../shared/evidence/README.md)

---

# Success Criteria

The Reporting tier is compliant when its capabilities consume canonical Findings, Risk, and
Evidence read-only, produce correlated, analyzed, mapped, generated, and bundled reports for
presentation, introduce no new schemas, treat output formats as serializations, and never create,
modify, or replace canonical Risk, Findings, or Evidence.
