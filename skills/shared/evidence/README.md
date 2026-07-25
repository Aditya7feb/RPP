# Evidence Shared Skill

**File:** `skills/shared/evidence/README.md`

**Version:** 1.0.0

---

# Purpose

The Evidence Shared Skill provides the canonical, implementation-independent
mechanism for capturing, storing, and referencing evidence within the Robust
PenTest Platform (RPP).

Rather than allowing individual skills and shared packages to persist artifacts
in their own way, this shared skill centralizes evidence capture, artifact
storage, integrity protection, redaction, and evidence referencing.

All packages that produce evidence SHALL do so through this shared skill.

---

# Goals

The Evidence Shared Skill SHALL

- Abstract evidence capture behind a stable interface
- Produce canonical [Evidence](../../../schemas/evidence.md) records
- Store associated artifacts by reference
- Guarantee integrity of stored evidence
- Redact secrets before persistence
- Enforce evidence scope and retention
- Enable correlation across findings, logs, and reports

---

# Non-Goals

The Evidence Shared Skill SHALL NOT

- Detect vulnerabilities
- Decide whether a finding is valid
- Interpret evidence as risk
- Perform target-facing operations
- Serve as an operational log substitute

Evidence records *what was observed*. Interpretation belongs to domain skills
producing [Findings](../../../schemas/finding.md); operational output belongs to
the [Logging](../logging/README.md) shared package.

---

# Design Principles

The Evidence Shared Skill SHALL be

- Deterministic in referencing
- Integrity preserving
- Scope aware
- Transport independent
- Observable
- Secure by default

---

# Architecture

```
Master Agent

↓

Domain Skill or Shared Package

↓

Evidence Shared Skill

├── Evidence Composer
├── Artifact Store
├── Integrity Sealer
├── Redaction Filter
├── Scope Guard
├── Retention Manager
├── Reference Manager

↓

Configured Artifact Backends
```

The Evidence Shared Skill composes and persists evidence but SHALL remain
unaware of artifact backend implementations.

---

# Responsibilities

The Evidence Shared Skill is responsible for

- Composing canonical [Evidence](../../../schemas/evidence.md) records
- Storing artifacts by reference
- Sealing evidence with integrity metadata
- Redacting secrets before persistence
- Enforcing evidence scope and retention
- Issuing stable evidence references
- Enabling correlation with findings, logs, and reports

---

# Evidence Lifecycle

```
Receive Capture Request

↓

Compose Evidence Record

↓

Store Artifacts (by reference)

↓

Apply Redaction

↓

Seal Integrity

↓

Persist Evidence

↓

Issue Evidence Reference

↓

Emit Events
```

Redaction SHALL precede sealing and persistence.

---

# Evidence Composition

The Evidence Shared Skill SHALL compose records conforming to the
[Evidence schema](../../../schemas/evidence.md), including inputs, outputs,
metadata, timings, and artifact references.

Composition SHALL be deterministic given the same capture request.

---

# Artifact Storage

Large payloads such as responses, captures, and archives SHALL be stored as
artifacts by reference rather than inline.

Artifact references SHALL be stable and SHALL resolve within the evidence scope.

---

# Integrity

The Evidence Shared Skill SHALL seal each evidence record with integrity
metadata, such as a content digest, so that tampering can be detected.

Sealed evidence SHALL be immutable. Corrections SHALL be expressed as new,
linked records rather than mutations.

---

# Redaction

The Evidence Shared Skill SHALL redact secret material before persistence.

Redaction SHALL apply to inputs, outputs, artifacts, and metadata.

Redacted fields SHALL be recorded so that auditors know redaction occurred.

Secrets SHALL never be persisted.

---

# Scope And Retention

The Evidence Shared Skill SHALL enforce evidence scope, bounding visibility to
the originating assessment unless policy permits broader reuse.

Retention SHALL be governed by configured policy. Expired evidence SHALL be
disposed of according to policy while preserving audit records of disposal.

---

# References

The Evidence Shared Skill SHALL issue stable evidence references that other
packages use to correlate

- [Findings](../../../schemas/finding.md)
- [Log Events](../../../schemas/log-event.md)
- [Reports](../../../schemas/report.md)

References SHALL remain valid for the lifetime of the evidence.

---

# Events

The Evidence Shared Skill SHOULD publish

- EvidenceCaptured
- ArtifactStored
- EvidenceSealed
- EvidenceRedacted
- EvidenceDisposed

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Evidence Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Evidence Shared Skill SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- All shared network packages
- All discovery, authentication, web-security, API, and cloud skills
- The [Reporting](../reporting/README.md) shared package
- Agent framework components

---

# Outputs

Typical outputs MAY include

- Sealed evidence records
- Artifact references
- Evidence references
- Evidence metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The Evidence Shared Skill SHALL

- Redact secrets before persistence
- Guarantee integrity and immutability of sealed evidence
- Enforce scope to prevent cross-assessment leakage
- Preserve a complete audit trail, including disposal
- Bound storage to prevent resource exhaustion

Evidence often contains sensitive material. The shared skill SHALL protect it
while preserving authenticity.

---

# Best Practices

Consumers SHOULD

- Capture evidence for every significant observation
- Store large payloads as artifacts by reference
- Reference evidence from findings and logs rather than duplicating it
- Choose the narrowest sufficient scope
- Rely on automatic redaction

---

# Anti-Patterns

Consumers SHOULD NOT

- Persist secrets in evidence
- Mutate sealed evidence
- Duplicate evidence across findings and logs
- Store large payloads inline
- Implement ad hoc artifact stores

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
- adr/ADR-001-evidence-abstraction.md

---

# Related Shared Packages

- [Logging](../logging/README.md)
- [Reporting](../reporting/README.md)
- [HTTP Client](../http-client/README.md)

---

# Canonical Schemas

- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Log Event](../../../schemas/log-event.md)
- [Report](../../../schemas/report.md)

---

# Architecture Decisions

- [ADR-001 — Evidence Abstraction](adr/ADR-001-evidence-abstraction.md)

---

# Future Extensions

Future versions MAY support

- Cryptographic evidence signing and chain-of-custody attestation
- Content-addressed artifact deduplication
- Tamper-evident append-only evidence ledgers
- Cross-assessment evidence federation under policy

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Evidence Shared Skill provides an integrity-preserving, scope-aware,
and implementation-independent evidence abstraction for the Robust PenTest
Platform.

It enables consistent, auditable evidence capture across every package while
protecting secrets and enabling correlation with findings, logs, and reports.
