# ADR-001 — Evidence Bundle Capability

**File:** `skills/reporting/evidence-bundle/adr/ADR-001-evidence-bundle-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Reports are accompanied by evidence bundles — self-contained, integrity-checked collections of the
Evidence that supports a report's Findings — for distribution to stakeholders. Assembling a bundle is
a Reporting-tier concern distinct from collecting evidence or owning its durable lifecycle. It must
remain read-only over Evidence and preserve integrity.

---

# Decision

We SHALL provide an Evidence Bundle Capability in the Reporting tier that loads referenced
[Evidence](../../../../schemas/evidence.md); verifies integrity references through the shared
[Evidence](../../../shared/evidence/README.md) infrastructure; redacts sensitive content for
distribution; assembles the bundle through the shared
[Reporting](../../../shared/reporting/README.md) package; records it as an
[Artifact](../../../../schemas/artifact.md) of type `evidence-bundle`; and emits
[Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk, modifies no Evidence, and
does not own the durable evidence lifecycle.

---

# Consequences

## Positive

- Distributable, integrity-preserving evidence bundles tied to report Findings.
- Read-only assembly preserves canonical ownership and the durable lifecycle boundary.

## Negative

- Bundle completeness depends on the availability and integrity of referenced Evidence.

## Neutral

- Encrypted, recipient-scoped bundles and chain-of-custody manifests are deferred to future
  extensions.

---

# Alternatives Considered

- Assembling bundles in the Evidence tier. Rejected because bundling for distribution is a Reporting
  concern; the Evidence tier owns collection and the durable lifecycle.
- Allowing the bundle to modify or re-capture Evidence. Rejected because Evidence is immutable to
  Reporting.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Evidence Schema](../../../../schemas/evidence.md)
- [Reporting](../../../shared/reporting/README.md)
