# ADR-001 — Report Generation Capability

**File:** `skills/reporting/report-generation/adr/ADR-001-report-generation-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments culminate in reports for different audiences — executive summaries and technical detail —
delivered in multiple output formats such as SARIF, JSON, Markdown, and PDF. Executive and technical
reports are audience variants of one generation concern, and the formats are serializations rather
than capabilities. Report generation is a Reporting-tier concern that consumes canonical objects
read-only and relies on the shared Reporting package for serialization.

---

# Decision

We SHALL provide a Report Generation Capability in the Reporting tier that consolidates executive and
technical report generation and all output formats. It loads referenced
[Findings](../../../../schemas/finding.md), [Risk](../../../../schemas/risk.md),
[Evidence](../../../../schemas/evidence.md), and correlation, analysis, and mapping content; composes
executive and technical reports; serializes [Reports](../../../../schemas/report.md) to SARIF, JSON,
Markdown, and PDF through the shared [Reporting](../../../shared/reporting/README.md) package; and
emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and modifies no
canonical objects.

---

# Consequences

## Positive

- One generation capability spanning audiences and formats rather than many packages.
- Formats remain serializations; audiences remain report types.

## Negative

- Report richness depends on the correlation, analysis, and mapping content supplied.

## Neutral

- Additional report types, formats, and localization are deferred to future extensions.

---

# Alternatives Considered

- Separate Executive Report and Technical Report packages, and separate SARIF/JSON/Markdown/PDF
  packages. Rejected because audiences are report types and formats are serializations, not
  capabilities.
- Serializing within the capability rather than the shared Reporting package. Rejected because
  rendering and serialization are shared primitives.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Report Schema](../../../../schemas/report.md)
- [Reporting](../../../shared/reporting/README.md)
