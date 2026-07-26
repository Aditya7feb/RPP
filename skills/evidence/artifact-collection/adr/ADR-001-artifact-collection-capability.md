# ADR-001 — Artifact Collection Capability

**File:** `skills/evidence/artifact-collection/adr/ADR-001-artifact-collection-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Assessments produce files, certificates, and other artifacts that must be collected as durable
evidence. File archival and certificate archival are the same collection concern applied to
different artifact types; modeling them as separate packages would fragment a single capability by
type rather than responsibility. Because archival is a shared Evidence lifecycle mechanic, the
capability is named for its responsibility — **collection** — and does not own the durable evidence
lifecycle.

---

# Decision

We SHALL provide an Artifact Collection Capability in the Evidence tier that consolidates file and
certificate collection. It reads artifacts through the
[Filesystem Client](../../../shared/filesystem-client/README.md); classifies them as `file`,
`certificate`, or other types, referencing the [Certificate](../../../../schemas/certificate.md)
and [Certificate Chain](../../../../schemas/certificate-chain.md) schemas for certificate artifacts;
records them as [Artifacts](../../../../schemas/artifact.md); invokes the shared
[Evidence](../../../shared/evidence/README.md) lifecycle to promote them into durable Evidence; and
emits [Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and does not own
durable persistence, integrity, or retention.

---

# Consequences

## Positive

- One collection capability spanning artifact types rather than per-type packages.
- The name reflects the responsibility (collection); archival remains a shared Evidence mechanic.

## Negative

- Collection fidelity depends on the shared Filesystem Client.

## Neutral

- Content-type-aware collection policies are deferred to future extensions.

---

# Alternatives Considered

- Separate File Archive and Certificate Archive packages. Rejected as type-only fragmentation.
- Naming the capability `artifact-archive`. Rejected because archival is a shared Evidence lifecycle
  mechanic; `collection` reflects the capability's responsibility and aligns with
  `screenshot-capture` and `log-collection`.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Filesystem Client](../../../shared/filesystem-client/README.md)
- [Evidence](../../../shared/evidence/README.md)
