# Finding Correlation Capability

**File:** `skills/reporting/finding-correlation/README.md`

**Version:** 1.0.0

---

# Purpose

The Finding Correlation Capability is a Reporting-tier capability that correlates, deduplicates, and
relates Findings for presentation within the Robust PenTest Platform (RPP).

It consumes canonical [Findings](../../../schemas/finding.md) read-only and produces correlation
results — deduplicated groups, related-finding links, and attack chains — that reference Findings by
identifier. It performs no vulnerability confirmation, creates no Findings, and owns no Risk.

The Finding Correlation Capability uses the shared
[Reporting](../../shared/reporting/README.md) package and produces
[Report](../../../schemas/report.md) content and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Finding Correlation Capability SHALL

- Deduplicate Findings that describe the same underlying issue
- Relate Findings that share a target, root cause, or attack path
- Construct attack chains from related Findings
- Reference [Findings](../../../schemas/finding.md) by identifier without modifying them
- Produce correlation content for [Reports](../../../schemas/report.md)
- Emit [Metrics](../../../schemas/metrics.md) describing correlation counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Finding Correlation Capability SHALL NOT

- Create, modify, or replace Findings, Risk, or Evidence
- Confirm vulnerabilities or interpret raw signals
- Classify or score Risk
- Capture evidence
- Invoke command-line tools or parse their output

Finding and Risk production belong to Domain Security capabilities; evidence belongs to the Evidence
tier; canonical Risk remains authoritative and immutable.

---

# Design Principles

The Finding Correlation Capability SHALL be

- Read-only over Findings
- Deterministic given the same Findings
- Reference-based rather than duplicating Finding content
- Traceable
- Implementation independent

---

# Architecture

```
Reporting Agent Or Workflow

↓

Finding Correlation Capability

├── Finding Loader        (Finding refs)
├── Deduplicator
├── Relator
├── Attack-Chain Builder
├── Correlation Writer    → Report content
└── Metrics Emitter       → Metrics

↓

Report Content · Metrics
```

The Finding Correlation Capability correlates references and SHALL NOT modify canonical objects.

---

# Responsibilities

The Finding Correlation Capability is responsible for

- Loading referenced [Findings](../../../schemas/finding.md)
- Deduplicating, relating, and chaining them
- Producing correlation content through the shared
  [Reporting](../../shared/reporting/README.md) package
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
finding_refs:

correlation:
  deduplicate:
  relate:
  build_chains:

bounds:
  max_findings:
```

`finding_refs` reference the Findings to correlate. `correlation` selects operations. `bounds`
limits scope.

---

# Outputs

Typical outputs MAY include

- Correlation content for a Report (deduplicated groups, related links, attack chains)
- Metrics describing correlation counts

Outputs SHALL reference canonical objects by identifier and SHALL contain no new Findings or Risk.

---

# Dependencies

The Finding Correlation Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Reporting](../../shared/reporting/README.md)
- [Finding Schema](../../../schemas/finding.md)
- [Report Schema](../../../schemas/report.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Finding Correlation Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Report Generation, which incorporates correlation content
- Reporting workflows

---

# Security Principles

The Finding Correlation Capability SHALL

- Treat Findings as immutable
- Reference canonical objects by identifier
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide the relevant set of Finding references
- Rely on correlation for presentation structure only
- Route Finding and Risk production to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect new Findings or Risk from this capability
- Expect modification of canonical objects
- Duplicate Finding content into correlation output

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
- adr/ADR-001-finding-correlation-capability.md

---

# Related Packages

- [Reporting](../../shared/reporting/README.md)
- [Report Generation](../report-generation/README.md)
- [Risk Analysis](../risk-analysis/README.md)

---

# Canonical Schemas

- [Finding](../../../schemas/finding.md)
- [Report](../../../schemas/report.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Finding Correlation Capability](adr/ADR-001-finding-correlation-capability.md)

---

# Future Extensions

Future versions MAY support

- Cross-assessment correlation
- Similarity-scored deduplication
- Kill-chain phase mapping

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Finding Correlation Capability deduplicates, relates, and chains Findings read-only and
produces correlation content that references canonical objects by identifier, without creating,
modifying, or replacing Findings, Risk, or Evidence.
