# Artifact Collection Capability

**File:** `skills/evidence/artifact-collection/README.md`

**Version:** 1.0.0

---

# Purpose

The Artifact Collection Capability is an Evidence-tier capability that collects files,
certificates, and other binary or structured artifacts as durable evidence within the Robust
PenTest Platform (RPP).

It gathers already-obtained artifacts — such as downloaded files, exported certificates, and
collected binaries — and records them as durable evidence by reference. It performs no
interpretation and produces no Findings.

The Artifact Collection Capability reads through the shared
[Filesystem Client](../../shared/filesystem-client/README.md), emits
[Artifacts](../../../schemas/artifact.md), and invokes the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote collected artifacts into durable
Evidence.

---

# Goals

The Artifact Collection Capability SHALL

- Collect files, certificates, and other artifacts as evidence
- Record collected items as [Artifacts](../../../schemas/artifact.md) of appropriate type
- Reference the [Certificate](../../../schemas/certificate.md) and
  [Certificate Chain](../../../schemas/certificate-chain.md) schemas for certificate artifacts
- Invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote artifacts
- Redact sensitive content where configured
- Bound collection volume and size
- Emit [Metrics](../../../schemas/metrics.md) describing collected artifact counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Artifact Collection Capability SHALL NOT

- Access the filesystem directly rather than through the shared Filesystem Client
- Interpret collected content or produce Findings or Risk
- Own durable persistence, integrity, or retention (that is the shared Evidence lifecycle)
- Collect artifacts from unauthorized locations
- Acquire certificates live from TLS or network interactions (that is TLS Analysis)
- Invoke command-line tools or parse their output

Filesystem access belongs to the shared Filesystem Client; interpretation belongs to Domain
Security capabilities; the durable evidence lifecycle belongs to the shared Evidence
infrastructure; live certificate acquisition belongs to TLS Analysis.

---

# Collection Scope

The Artifact Collection Capability is intentionally limited to **filesystem-available artifacts**:
files, locally available or exported certificates, and other artifacts already present at an
authorized filesystem location. It reads these exclusively through the shared
[Filesystem Client](../../shared/filesystem-client/README.md).

The Artifact Collection Capability SHALL NOT perform **live certificate acquisition** from TLS or
network interactions. Acquiring certificates directly from a live TLS handshake or network exchange
is the responsibility of the [TLS Analysis](../../discovery/tls-analysis/README.md) discovery skill,
which uses the shared [TLS Client](../../shared/tls-client/README.md) and produces certificate
Assets and Evidence. Certificates obtained live by TLS Analysis MAY subsequently be collected by
this capability from an authorized filesystem location as durable artifact evidence.

This boundary removes ownership ambiguity: **live acquisition belongs to TLS Analysis; filesystem
collection and durable artifact recording belong here.** Because collection is confined to the
filesystem, this capability depends on the [Filesystem Client](../../shared/filesystem-client/README.md)
and does not depend on the TLS or network transport clients.

---

# Design Principles

The Artifact Collection Capability SHALL be

- Scope-confined to authorized locations
- Faithful to collected content
- Bounded in volume and size
- Redaction-aware
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

Artifact Collection Capability

├── Location Confiner
├── Artifact Reader        → Filesystem Client
├── Type Classifier        (file · certificate · other)
├── Redactor
├── Artifact Writer        → Artifact
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Artifacts · Evidence · Metrics
```

The Artifact Collection Capability collects artifacts and SHALL remain unaware of the filesystem
implementation.

---

# Responsibilities

The Artifact Collection Capability is responsible for

- Confining collection to authorized locations
- Reading artifacts through the [Filesystem Client](../../shared/filesystem-client/README.md)
- Classifying and recording artifacts as [Artifacts](../../../schemas/artifact.md)
- Invoking the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote artifacts
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
sources:

types:

bounds:
  max_artifacts:
  max_size_bytes:

redaction:

scope_id:

roe_id:
```

`sources` reference authorized locations. `types` selects artifact types such as `file` or
`certificate`. `bounds` limits collection.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `file`, `certificate`, or other collected types
- Evidence references produced through the shared lifecycle
- Metrics describing collected artifact counts

Outputs SHALL contain no Findings or Risk.

---

# Authorization

The Artifact Collection Capability SHALL collect only from authorized locations referenced by
`sources` and within the assessment [Scope](../../../schemas/scope.md). Collection SHALL be bounded
in volume and size. Unauthorized locations SHALL never be collected.

---

# Dependencies

The Artifact Collection Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Filesystem Client](../../shared/filesystem-client/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Certificate Schema](../../../schemas/certificate.md)
- [Certificate Chain Schema](../../../schemas/certificate-chain.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Artifact Collection Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills requiring file or certificate evidence
- Reporting, through promoted Evidence
- Timeline, which correlates collected artifacts

---

# Security Principles

The Artifact Collection Capability SHALL

- Collect only from authorized, in-scope locations
- Bound collection volume and size
- Redact sensitive content where configured
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide authorized source locations and bounded selection
- Rely on the shared Evidence lifecycle for durability
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Access the filesystem directly
- Collect from unauthorized locations
- Expect interpretation or findings from this capability

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
- adr/ADR-001-artifact-collection-capability.md

---

# Related Packages

- [Filesystem Client](../../shared/filesystem-client/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Timeline](../timeline/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Certificate](../../../schemas/certificate.md)
- [Certificate Chain](../../../schemas/certificate-chain.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Artifact Collection Capability](adr/ADR-001-artifact-collection-capability.md)

---

# Future Extensions

Future versions MAY support

- Content-type-aware collection policies
- Provenance-linked collection
- Deduplicated artifact collection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Artifact Collection Capability collects files, certificates, and other artifacts from
authorized locations within bounds and invokes the shared Evidence lifecycle for durability,
without interpreting content or producing Findings or Risk.
