# Report Generation Capability

**File:** `skills/reporting/report-generation/README.md`

**Version:** 1.0.0

---

# Purpose

The Report Generation Capability is a Reporting-tier capability that generates executive and
technical reports from canonical Findings, Risk, and Evidence within the Robust PenTest Platform
(RPP).

It consumes canonical [Findings](../../../schemas/finding.md),
[Risk](../../../schemas/risk.md), and [Evidence](../../../schemas/evidence.md) read-only, together
with correlation, analysis, and mapping content, and produces [Reports](../../../schemas/report.md)
serialized to the required output formats. It creates no Findings, owns no Risk, and modifies no
canonical objects.

The Report Generation Capability uses the shared
[Reporting](../../shared/reporting/README.md) package for rendering and serialization, and emits
[Metrics](../../../schemas/metrics.md).

---

# Goals

The Report Generation Capability SHALL

- Generate executive reports for stakeholder audiences
- Generate technical reports for practitioner audiences
- Incorporate correlation, risk-analysis, and mapping content
- Reference canonical [Findings](../../../schemas/finding.md),
  [Risk](../../../schemas/risk.md), and [Evidence](../../../schemas/evidence.md) by identifier
- Serialize [Reports](../../../schemas/report.md) to SARIF, JSON, Markdown, and PDF through the
  shared [Reporting](../../shared/reporting/README.md) package
- Emit [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Report Generation Capability SHALL NOT

- Create, modify, or replace Findings, Risk, or Evidence
- Confirm vulnerabilities or produce Findings
- Own canonical Risk
- Treat output formats as distinct capabilities
- Invoke command-line tools or parse their output

Finding and Risk production belong to Domain Security capabilities; rendering and serialization
primitives belong to the shared Reporting package; canonical objects remain immutable.

---

# Output Formats

Report output formats — **SARIF, JSON, Markdown, and PDF** — are serializations of a generated
Report, produced through the shared [Reporting](../../shared/reporting/README.md) package. No format
is a separate capability. A single Report MAY be serialized to multiple formats.

---

# Design Principles

The Report Generation Capability SHALL be

- Read-only over Findings, Risk, and Evidence
- Deterministic given the same inputs and template
- Reference-based rather than duplicating canonical content
- Audience-aware (executive and technical)
- Implementation independent

---

# Architecture

```
Reporting Agent Or Workflow

↓

Report Generation Capability

├── Input Loader          (Findings · Risk · Evidence · correlation · analysis · mapping)
├── Executive Composer
├── Technical Composer
├── Serializer            → Reporting (SARIF · JSON · Markdown · PDF)
├── Report Writer         → Report
└── Metrics Emitter       → Metrics

↓

Reports · Metrics
```

The Report Generation Capability composes reports and SHALL remain unaware of serialization
implementations, which are provided by the shared Reporting package.

---

# Responsibilities

The Report Generation Capability is responsible for

- Loading canonical [Findings](../../../schemas/finding.md),
  [Risk](../../../schemas/risk.md), and [Evidence](../../../schemas/evidence.md) and reporting
  content
- Composing executive and technical reports
- Serializing [Reports](../../../schemas/report.md) through the shared
  [Reporting](../../shared/reporting/README.md) package
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
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

`report_type` selects `executive` or `technical`. `content` references correlation, analysis, and
mapping content. `formats` selects output serializations. `template_ref` references a report
template.

---

# Outputs

Typical outputs MAY include

- A generated [Report](../../../schemas/report.md) referencing canonical objects by identifier
- Serializations in the requested formats
- Metrics describing generation

Outputs SHALL reference canonical objects by identifier and SHALL contain no new Findings or Risk.

---

# Dependencies

The Report Generation Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Reporting](../../shared/reporting/README.md)
- [Report Schema](../../../schemas/report.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Report Generation Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Reporting workflows and the Master Agent
- Stakeholders receiving reports

---

# Security Principles

The Report Generation Capability SHALL

- Treat Findings, Risk, and Evidence as immutable
- Reference canonical objects by identifier
- Distinguish derived analysis figures from canonical Risk
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide correlation, analysis, and mapping content for richer reports
- Select the appropriate report type and formats
- Rely on the shared Reporting package for serialization

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect new Findings or Risk from this capability
- Expect modification of canonical objects
- Treat output formats as separate capabilities

---

# Documentation Requirements

This capability includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-report-generation-capability.md

---

# Related Packages

- [Reporting](../../shared/reporting/README.md)
- [Finding Correlation](../finding-correlation/README.md)
- [Risk Analysis](../risk-analysis/README.md)
- [Finding Mapping](../finding-mapping/README.md)
- [Evidence Bundle](../evidence-bundle/README.md)

---

# Canonical Schemas

- [Report](../../../schemas/report.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Report Generation Capability](adr/ADR-001-report-generation-capability.md)

---

# Future Extensions

Future versions MAY support

- Additional report types
- Additional serialization formats
- Templated branding and localization

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Report Generation Capability generates executive and technical reports read-only from
canonical objects and serializes them to the required formats through the shared Reporting package,
without creating, modifying, or replacing Findings, Risk, or Evidence, and without treating formats
as separate capabilities.
