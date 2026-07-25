# Reporting Shared Skill

**File:** `skills/shared/reporting/README.md`

**Version:** 1.0.0

---

# Purpose

The Reporting Shared Skill provides the canonical, implementation-independent
mechanism for composing assessment reports within the Robust PenTest Platform
(RPP).

Rather than allowing individual skills to assemble reports in their own way, this
shared skill centralizes finding aggregation, deduplication, correlation,
evidence bundling, severity ordering, and report rendering into canonical output
formats.

All packages that contribute to reporting SHALL do so through this shared skill.

---

# Goals

The Reporting Shared Skill SHALL

- Abstract report composition behind a stable interface
- Aggregate canonical [Findings](../../../schemas/finding.md)
- Deduplicate and correlate related findings
- Bundle referenced [Evidence](../../../schemas/evidence.md)
- Order findings by severity and confidence
- Render canonical [Reports](../../../schemas/report.md) in multiple formats
- Preserve traceability from report to evidence

---

# Non-Goals

The Reporting Shared Skill SHALL NOT

- Detect vulnerabilities
- Assign risk beyond applying declared scoring inputs
- Produce findings itself
- Perform target-facing operations
- Persist evidence in place of the Evidence package

Reporting *composes* what domain skills produced. It SHALL NOT create findings
or reinterpret their validity.

---

# Design Principles

The Reporting Shared Skill SHALL be

- Deterministic given the same inputs
- Traceable to evidence
- Format independent at the model layer
- Correlation aware
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Reporting Shared Skill

├── Finding Aggregator
├── Deduplicator
├── Correlator
├── Severity Orderer
├── Evidence Bundler
├── Report Composer
├── Renderer

↓

Canonical Report + Rendered Outputs
```

The Reporting Shared Skill composes a canonical report model and renders it
through format adapters. It SHALL remain unaware of renderer implementations.

---

# Responsibilities

The Reporting Shared Skill is responsible for

- Aggregating [Findings](../../../schemas/finding.md) across skills
- Deduplicating findings that describe the same issue
- Correlating related findings into logical groups
- Ordering findings by severity and confidence
- Bundling referenced [Evidence](../../../schemas/evidence.md)
- Composing a canonical [Report](../../../schemas/report.md)
- Rendering the report into requested formats

---

# Reporting Lifecycle

```
Receive Compose Request

↓

Aggregate Findings

↓

Deduplicate

↓

Correlate

↓

Order By Severity And Confidence

↓

Bundle Evidence

↓

Compose Canonical Report

↓

Render Outputs

↓

Emit Events
```

The composition SHOULD be reproducible from the same inputs.

---

# Finding Aggregation

The Reporting Shared Skill SHALL aggregate findings conforming to the
[Finding schema](../../../schemas/finding.md) from every contributing skill
within an assessment.

Aggregation SHALL preserve each finding's provenance.

---

# Deduplication

The Reporting Shared Skill SHALL deduplicate findings that describe the same
issue at the same location.

Deduplication SHALL merge evidence references rather than discard them.

The retained finding SHALL preserve the highest confidence and severity among
duplicates.

---

# Correlation

The Reporting Shared Skill SHALL correlate related findings into logical groups,
such as multiple injection points of one vulnerability class.

Correlation SHALL NOT alter individual finding validity.

---

# Severity Ordering

The Reporting Shared Skill SHALL order findings primarily by severity and
secondarily by confidence, using the scoring inputs declared on each finding.

The shared skill SHALL apply, but SHALL NOT invent, risk scores.

---

# Evidence Bundling

The Reporting Shared Skill SHALL bundle evidence referenced by included findings
through the [Evidence](../evidence/README.md) shared package.

Bundled evidence SHALL be referenced, not duplicated, and SHALL preserve
integrity and redaction guarantees.

---

# Report Composition

The Reporting Shared Skill SHALL compose a canonical
[Report](../../../schemas/report.md) containing summary, findings, correlations,
and evidence references.

The canonical report SHALL be format independent.

---

# Rendering

The Reporting Shared Skill SHALL render the canonical report into requested
formats through adapters.

Supported output families include

- structured (such as JSON and SARIF)
- document (such as Markdown and PDF)

Renderer implementations SHALL remain hidden behind adapters.

---

# Events

The Reporting Shared Skill SHOULD publish

- ReportCompositionStarted
- FindingsAggregated
- FindingsDeduplicated
- EvidenceBundled
- ReportComposed
- ReportRendered

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Reporting Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence](../evidence/README.md)
- [Finding Schema](../../../schemas/finding.md)
- [Report Schema](../../../schemas/report.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Reporting Shared Skill SHALL NOT depend on domain skills. Domain skills
produce findings that reporting consumes.

---

# Consumers

Typical consumers include

- The Master Agent report-merging process
- Assessment finalization workflows
- Export and delivery components

---

# Outputs

Typical outputs MAY include

- A canonical report model
- Rendered report documents
- Evidence bundles
- Reporting metrics

Outputs SHALL remain implementation independent at the model layer.

---

# Security Principles

The Reporting Shared Skill SHALL

- Preserve evidence integrity and redaction in bundles
- Avoid duplicating secrets into rendered outputs
- Preserve provenance and traceability
- Apply only declared risk scores
- Bound report size to prevent resource exhaustion

Reports are often shared externally. The shared skill SHALL ensure rendered
output never exposes redacted material.

---

# Best Practices

Consumers SHOULD

- Submit findings conforming to the Finding schema
- Reference evidence rather than embedding it
- Rely on deduplication and correlation
- Request only the formats needed
- Preserve traceability to evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Assemble reports outside the shared skill
- Embed unredacted evidence in reports
- Reinterpret finding validity during reporting
- Invent risk scores
- Duplicate evidence payloads

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-reporting-abstraction.md

---

# Related Shared Packages

- [Evidence](../evidence/README.md)
- [Logging](../logging/README.md)

---

# Canonical Schemas

- [Report](../../../schemas/report.md)
- [Finding](../../../schemas/finding.md)
- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Reporting Abstraction](adr/ADR-001-reporting-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Delta reporting across assessments
- Customizable report templates expressed as canonical descriptors
- Standards mappings such as OWASP and MITRE ATT&CK enrichment
- Multi-language rendering

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Reporting Shared Skill provides a deterministic, traceable, and
implementation-independent reporting abstraction for the Robust PenTest
Platform.

It enables consistent aggregation, correlation, and rendering of findings across
every skill while preserving evidence integrity and never exposing redacted
material.
