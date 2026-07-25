# ADR-001 — Evidence Abstraction

**File:** `skills/shared/evidence/adr/ADR-001-evidence-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The Robust PenTest Platform must produce trustworthy, auditable evidence for
every significant observation. Evidence underpins findings, reports, and the
overall credibility of an assessment. Evidence handling carries several
requirements:

- Integrity, so that evidence cannot be silently altered
- Redaction, so that secrets are never persisted
- Scope, so that evidence does not leak across assessments
- Correlation, so that findings, logs, and reports reference the same source
- Retention, so that evidence is disposed of responsibly

Before this decision, packages could persist artifacts independently. That
approach produced inconsistent formats, no integrity guarantees, risk of secret
persistence, and no reliable way to correlate evidence across the platform.

The platform requires a single, canonical, implementation-independent mechanism
to capture and reference evidence.

---

# Decision

The platform SHALL provide a dedicated Evidence shared skill that centralizes all
evidence capture, storage, and referencing behind a stable interface.

The Evidence shared skill SHALL

- Compose canonical [Evidence](../../../../schemas/evidence.md) records
- Store large payloads as artifacts by reference
- Seal evidence with integrity metadata and treat it as immutable
- Redact secrets before persistence, unconditionally
- Enforce scope and retention
- Issue stable references correlating
  [Findings](../../../../schemas/finding.md),
  [Log Events](../../../../schemas/log-event.md), and
  [Reports](../../../../schemas/report.md)

Consumers SHALL capture evidence exclusively through the
[Evidence Interface](../interface.md). Backend implementations SHALL remain
hidden behind adapters.

---

# Alternatives Considered

## Per-Package Artifact Storage

Each package could persist its own artifacts.

Rejected because it produces inconsistent formats, no integrity guarantees, and
risk of secret persistence, with no reliable correlation.

## Logs As Evidence

Operational logs could serve as evidence.

Rejected because logs and evidence have different guarantees and lifecycles.
Evidence is sealed, immutable, and authoritative; logs are observability
records. The [Logging](../../logging/README.md) shared package and the Evidence
shared skill remain distinct and complementary.

## Inline Evidence In Findings

Evidence could be embedded directly in findings.

Rejected because it duplicates large payloads, prevents integrity sealing, and
couples finding size to evidence size. Reference-based correlation is superior.

---

# Consequences

## Positive

- Uniform, sealed, immutable evidence across every package
- Guaranteed redaction of secrets before persistence
- Scope isolation preventing cross-assessment leakage
- Reliable correlation across findings, logs, and reports
- Responsible retention with audited disposal

## Negative

- Consumers MUST capture evidence through the interface
- An additional shared dependency is introduced
- Integrity sealing and redaction add capture overhead

The negative consequences are outweighed by the trust, safety, and
auditability benefits.

---

# Compliance

Consumers SHALL

- Capture evidence through the Evidence Interface
- Store large payloads as artifacts by reference
- Reference evidence from findings and logs rather than duplicating it
- Never place secrets in evidence

Packages that produce evidence SHALL depend on the Evidence shared skill and
SHALL NOT implement independent artifact stores.

---

# Future Compatibility

Future versions MAY introduce cryptographic signing, chain-of-custody
attestation, and append-only evidence ledgers. These extensions SHALL preserve
the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Evidence README](../README.md)
- [Evidence Interface](../interface.md)
- [Evidence Execution Model](../execution.md)
- [Evidence Error Model](../error-model.md)
- [Evidence Schema](../../../../schemas/evidence.md)
- [Logging](../../logging/README.md)
- [Finding Schema](../../../../schemas/finding.md)
