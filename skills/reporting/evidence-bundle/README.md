# Evidence Bundle Capability

**File:** `skills/reporting/evidence-bundle/README.md`

**Version:** 1.0.0

---

# Purpose

The Evidence Bundle Capability is a Reporting-tier capability that assembles referenced Evidence into
a distributable bundle within the Robust PenTest Platform (RPP).

It consumes canonical [Evidence](../../../schemas/evidence.md) read-only — typically the Evidence
referenced by a report's Findings — and assembles a self-contained, integrity-checked bundle for
distribution. It modifies no Evidence, creates no Findings, and owns no Risk.

The Evidence Bundle Capability uses the shared [Reporting](../../shared/reporting/README.md) package
and the shared [Evidence](../../shared/evidence/README.md) infrastructure, and emits
[Metrics](../../../schemas/metrics.md).

---

# Goals

The Evidence Bundle Capability SHALL

- Assemble referenced [Evidence](../../../schemas/evidence.md) into a distributable bundle
- Preserve evidence integrity references within the bundle
- Reference Findings and Evidence by identifier without modifying them
- Redact sensitive content where required for distribution
- Produce the bundle as an [Artifact](../../../schemas/artifact.md)
- Emit [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Evidence Bundle Capability SHALL NOT

- Create, modify, or replace Evidence, Findings, or Risk
- Capture evidence or own the durable evidence lifecycle
- Confirm vulnerabilities or produce Findings
- Invoke command-line tools or parse their output

Evidence collection and the durable lifecycle belong to the Evidence tier and shared Evidence
infrastructure; Finding and Risk production belong to Domain Security capabilities.

---

# Design Principles

The Evidence Bundle Capability SHALL be

- Read-only over Evidence
- Integrity-preserving
- Reference-based, assembling by reference
- Redaction-aware for distribution
- Implementation independent

---

# Architecture

```
Reporting Agent Or Workflow

↓

Evidence Bundle Capability

├── Evidence Loader       (Evidence refs)
├── Integrity Verifier    → Evidence (shared)
├── Redactor
├── Bundle Assembler      → Reporting (shared)
├── Bundle Writer         → Artifact
└── Metrics Emitter       → Metrics

↓

Bundle Artifact · Metrics
```

The Evidence Bundle Capability assembles evidence and SHALL NOT modify canonical objects.

---

# Responsibilities

The Evidence Bundle Capability is responsible for

- Loading referenced [Evidence](../../../schemas/evidence.md)
- Verifying integrity references through the shared
  [Evidence](../../shared/evidence/README.md) infrastructure
- Redacting sensitive content where required for distribution
- Assembling the bundle through the shared
  [Reporting](../../shared/reporting/README.md) package and recording it as an
  [Artifact](../../../schemas/artifact.md)
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
evidence_refs:

finding_refs:

redaction:

bounds:
  max_evidence:
  max_size_bytes:
```

`evidence_refs` reference the Evidence to bundle. `finding_refs` MAY scope the bundle to a report's
Findings. `redaction` configures distribution redaction. `bounds` limits bundle size.

---

# Outputs

Typical outputs MAY include

- A bundle [Artifact](../../../schemas/artifact.md) of type `evidence-bundle`
- Metrics describing bundle contents

Outputs SHALL reference canonical objects by identifier and SHALL contain no new Findings or Risk.

---

# Dependencies

The Evidence Bundle Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Reporting](../../shared/reporting/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Evidence Bundle Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Report Generation, which references bundles
- Stakeholders receiving evidence bundles

---

# Security Principles

The Evidence Bundle Capability SHALL

- Treat Evidence as immutable
- Preserve evidence integrity references
- Redact sensitive content where required for distribution
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide the Evidence referenced by a report's Findings
- Apply distribution redaction where required
- Rely on the shared Evidence infrastructure for integrity

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect new Findings or Risk from this capability
- Expect modification of canonical Evidence
- Capture new evidence through this capability

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
- adr/ADR-001-evidence-bundle-capability.md

---

# Related Packages

- [Reporting](../../shared/reporting/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Report Generation](../report-generation/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Evidence Bundle Capability](adr/ADR-001-evidence-bundle-capability.md)

---

# Future Extensions

Future versions MAY support

- Encrypted, recipient-scoped bundles
- Selective evidence inclusion policies
- Chain-of-custody manifests

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Evidence Bundle Capability assembles referenced Evidence into an integrity-preserving,
distributable bundle read-only, referencing canonical objects by identifier, without creating,
modifying, or replacing Evidence, Findings, or Risk, and without owning the durable evidence
lifecycle.
