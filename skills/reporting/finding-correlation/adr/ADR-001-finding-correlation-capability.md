# ADR-001 — Finding Correlation Capability

**File:** `skills/reporting/finding-correlation/adr/ADR-001-finding-correlation-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Reports require a correlated view of Findings — deduplicated groups, related findings, and attack
chains — so that stakeholders see a coherent picture rather than a raw list. Correlating Findings is
a Reporting-tier concern distinct from producing them. It must remain read-only: Findings, Risk, and
Evidence are immutable and owned elsewhere.

---

# Decision

We SHALL provide a Finding Correlation Capability in the Reporting tier that loads referenced
[Findings](../../../../schemas/finding.md); deduplicates, relates, and chains them; produces
correlation content for a [Report](../../../../schemas/report.md) through the shared
[Reporting](../../../shared/reporting/README.md) package; and emits
[Metrics](../../../../schemas/metrics.md). It references canonical objects by identifier and does not
create, modify, or replace Findings, Risk, or Evidence.

---

# Consequences

## Positive

- A coherent, deduplicated, chained view of Findings for reports.
- Read-only correlation preserves canonical ownership and immutability.

## Negative

- Correlation quality depends on Finding metadata completeness.

## Neutral

- Cross-assessment correlation is deferred to future extensions.

---

# Alternatives Considered

- Correlating within Domain Security. Rejected because correlation is a presentation concern spanning
  Findings from multiple domain capabilities.
- Allowing correlation to merge or modify Findings. Rejected because Findings are immutable and owned
  by Domain Security.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Reporting](../../../shared/reporting/README.md)
- [Finding Schema](../../../../schemas/finding.md)
