# Risk Analysis Capability

**File:** `skills/reporting/risk-analysis/README.md`

**Version:** 1.0.0

---

# Purpose

The Risk Analysis Capability is a Reporting-tier capability that performs presentation and analytical
risk functions over Findings and canonical Risk within the Robust PenTest Platform (RPP).

It consumes canonical [Findings](../../../schemas/finding.md) and
[Risk](../../../schemas/risk.md) read-only and produces derived, presentation-only figures — CVSS
vectors, normalized scores, aggregate risk, prioritization, and portfolio metrics. **It does not own,
create, modify, or replace canonical Risk.** Domain Security owns canonical Risk, which remains
authoritative.

The Risk Analysis Capability uses the shared
[Reporting](../../shared/reporting/README.md) package and produces
[Report](../../../schemas/report.md) content and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Risk Analysis Capability SHALL

- Calculate CVSS vectors for presentation where required
- Normalize scores across Findings for comparison
- Aggregate risk across Findings and scopes
- Prioritize Findings for presentation
- Compute portfolio-level risk metrics
- Reference canonical [Risk](../../../schemas/risk.md) as authoritative
- Produce risk-analysis content for [Reports](../../../schemas/report.md)
- Emit [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings and own no canonical Risk

---

# Non-Goals

The Risk Analysis Capability SHALL NOT

- Create, modify, or replace canonical [Risk](../../../schemas/risk.md)
- Modify Findings or Evidence
- Confirm vulnerabilities or produce Findings
- Present a derived value as if it were canonical Risk
- Invoke command-line tools or parse their output

Confirmation of vulnerabilities and production of canonical Risk belong to Domain Security
capabilities; canonical Risk remains authoritative and immutable.

---

# Canonical Risk Authority

Domain Security owns canonical [Risk](../../../schemas/risk.md). The Risk Analysis Capability MAY
calculate CVSS vectors, normalize scores, aggregate risk, prioritize Findings, and compute
portfolio-level metrics for presentation. These are analytical, presentation-only functions. **Where
a calculated value differs from the canonical Risk, the canonical Risk remains authoritative**, and
the calculated value SHALL be presented as a derived figure clearly distinguished from canonical
Risk.

---

# Design Principles

The Risk Analysis Capability SHALL be

- Read-only over Findings and Risk
- Deterministic given the same inputs
- Transparent — derived values are clearly distinguished from canonical Risk
- Reference-based
- Implementation independent

---

# Architecture

```
Reporting Agent Or Workflow

↓

Risk Analysis Capability

├── Finding And Risk Loader   (refs)
├── CVSS Calculator           (presentation)
├── Score Normalizer
├── Risk Aggregator
├── Prioritizer
├── Portfolio-Metrics Computer
├── Analysis Writer           → Report content
└── Metrics Emitter           → Metrics

↓

Report Content · Metrics
```

The Risk Analysis Capability derives presentation figures and SHALL NOT modify canonical objects.

---

# Responsibilities

The Risk Analysis Capability is responsible for

- Loading referenced [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md)
- Calculating CVSS, normalizing, aggregating, and prioritizing for presentation
- Computing portfolio-level metrics
- Producing analysis content through the shared
  [Reporting](../../shared/reporting/README.md) package
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
finding_refs:

risk_refs:

analysis:
  calculate_cvss:
  normalize:
  aggregate:
  prioritize:
  portfolio_metrics:

bounds:
  max_findings:
```

`finding_refs` and `risk_refs` reference inputs. `analysis` selects functions. `bounds` limits scope.

---

# Outputs

Typical outputs MAY include

- Derived, presentation-only CVSS vectors and normalized scores
- Aggregate and prioritized risk views
- Portfolio-level risk metrics
- Report content and Metrics

Outputs SHALL reference canonical objects by identifier, SHALL distinguish derived values from
canonical Risk, and SHALL contain no new Findings or canonical Risk.

---

# Dependencies

The Risk Analysis Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Reporting](../../shared/reporting/README.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)
- [Report Schema](../../../schemas/report.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Risk Analysis Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Report Generation, which incorporates risk-analysis content
- Reporting workflows

---

# Security Principles

The Risk Analysis Capability SHALL

- Treat Findings and canonical Risk as immutable
- Present derived values as derived, never as canonical Risk
- Preserve the authority of canonical Risk
- Produce no Findings or canonical Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide the relevant Finding and Risk references
- Treat calculated CVSS and scores as presentation figures
- Rely on Domain Security for authoritative Risk

---

# Anti-Patterns

Consumers SHOULD NOT

- Treat derived values as canonical Risk
- Expect this capability to create or modify Risk
- Modify canonical objects

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
- adr/ADR-001-risk-analysis-capability.md

---

# Related Packages

- [Reporting](../../shared/reporting/README.md)
- [Finding Correlation](../finding-correlation/README.md)
- [Report Generation](../report-generation/README.md)

---

# Canonical Schemas

- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)
- [Report](../../../schemas/report.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Risk Analysis Capability](adr/ADR-001-risk-analysis-capability.md)

---

# Future Extensions

Future versions MAY support

- Additional scoring frameworks
- Trend and time-series risk analysis
- Configurable prioritization models

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Risk Analysis Capability calculates CVSS, normalizes, aggregates, prioritizes, and
computes portfolio metrics read-only for presentation, always preserving the authority of
Domain-owned canonical Risk and never creating, modifying, or replacing it.
