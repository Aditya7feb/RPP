# Finding Mapping Capability

**File:** `skills/reporting/finding-mapping/README.md`

**Version:** 1.0.0

---

# Purpose

The Finding Mapping Capability is a Reporting-tier capability that enriches Findings with standards
mappings for presentation within the Robust PenTest Platform (RPP).

It consumes canonical [Findings](../../../schemas/finding.md) read-only and produces mapping
enrichment — OWASP category mappings and MITRE ATT&CK technique mappings — that reference Findings by
identifier. It performs no vulnerability confirmation, creates no Findings, and owns no Risk.

The Finding Mapping Capability uses the shared
[Reporting](../../shared/reporting/README.md) package and produces
[Report](../../../schemas/report.md) content and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Finding Mapping Capability SHALL

- Map Findings to OWASP categories for presentation
- Map Findings to MITRE ATT&CK techniques for presentation
- Reference existing classification present on Findings, such as CWE, without altering it
- Reference [Findings](../../../schemas/finding.md) by identifier without modifying them
- Produce mapping content for [Reports](../../../schemas/report.md)
- Emit [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Finding Mapping Capability SHALL NOT

- Create, modify, or replace Findings, Risk, or Evidence
- Confirm vulnerabilities or produce Findings
- Classify or score Risk
- Invoke command-line tools or parse their output

Finding classification and production belong to Domain Security capabilities; canonical Risk remains
authoritative and immutable.

---

# Design Principles

The Finding Mapping Capability SHALL be

- Read-only over Findings
- Deterministic given the same Findings and mapping references
- Reference-based
- Traceable to mapping sources
- Implementation independent

---

# Architecture

```
Reporting Agent Or Workflow

↓

Finding Mapping Capability

├── Finding Loader        (Finding refs)
├── OWASP Mapper
├── MITRE ATT&CK Mapper
├── Mapping Writer        → Report content
└── Metrics Emitter       → Metrics

↓

Report Content · Metrics
```

The Finding Mapping Capability enriches references and SHALL NOT modify canonical objects.

---

# Responsibilities

The Finding Mapping Capability is responsible for

- Loading referenced [Findings](../../../schemas/finding.md)
- Mapping them to OWASP categories and MITRE ATT&CK techniques for presentation
- Producing mapping content through the shared
  [Reporting](../../shared/reporting/README.md) package
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
finding_refs:

mapping:
  owasp:
  mitre_attack:

bounds:
  max_findings:
```

`finding_refs` reference the Findings to map. `mapping` selects mapping frameworks. `bounds` limits
scope.

---

# Outputs

Typical outputs MAY include

- OWASP and MITRE ATT&CK mapping content referencing Findings by identifier
- Metrics describing mapping counts

Outputs SHALL reference canonical objects by identifier and SHALL contain no new Findings or Risk.

---

# Dependencies

The Finding Mapping Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Reporting](../../shared/reporting/README.md)
- [Finding Schema](../../../schemas/finding.md)
- [Report Schema](../../../schemas/report.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Finding Mapping Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Report Generation, which incorporates mapping content
- Reporting workflows

---

# Security Principles

The Finding Mapping Capability SHALL

- Treat Findings as immutable
- Reference canonical objects and mapping sources
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide the relevant Finding references
- Rely on mapping for presentation enrichment only
- Route Finding classification to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect new Findings or Risk from this capability
- Expect modification of canonical objects
- Treat presentation mappings as authoritative classification changes

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
- adr/ADR-001-finding-mapping-capability.md

---

# Related Packages

- [Reporting](../../shared/reporting/README.md)
- [Report Generation](../report-generation/README.md)
- [Finding Correlation](../finding-correlation/README.md)

---

# Canonical Schemas

- [Finding](../../../schemas/finding.md)
- [Report](../../../schemas/report.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Finding Mapping Capability](adr/ADR-001-finding-mapping-capability.md)

---

# Future Extensions

Future versions MAY support

- Additional mapping frameworks
- Compliance-control mappings
- Coverage summaries against a framework

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Finding Mapping Capability enriches Findings with OWASP and MITRE ATT&CK mappings
read-only for presentation, referencing canonical objects by identifier, without creating,
modifying, or replacing Findings, Risk, or Evidence.
