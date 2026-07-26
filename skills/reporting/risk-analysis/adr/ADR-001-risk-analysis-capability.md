# ADR-001 — Risk Analysis Capability

**File:** `skills/reporting/risk-analysis/adr/ADR-001-risk-analysis-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Reports require CVSS vectors, normalized and aggregated scores, prioritization, and portfolio-level
risk metrics. These are analytical and presentation functions distinct from producing canonical
Risk. Canonical Risk is owned by Domain Security and is authoritative; a Reporting capability must
compute derived figures without owning, creating, modifying, or replacing canonical Risk.

The capability is named **risk-analysis** rather than **risk-scoring** because "scoring" implies
ownership of Risk, whereas the capability performs normalization, aggregation, prioritization, and
presentation analysis. CVSS is one analytical method within this capability.

---

# Decision

We SHALL provide a Risk Analysis Capability in the Reporting tier that loads referenced
[Findings](../../../../schemas/finding.md) and [Risk](../../../../schemas/risk.md); calculates CVSS
vectors, normalizes scores, aggregates risk, prioritizes Findings, and computes portfolio-level
metrics for presentation; produces analysis content for a [Report](../../../../schemas/report.md)
through the shared [Reporting](../../../shared/reporting/README.md) package; and emits
[Metrics](../../../../schemas/metrics.md).

The capability SHALL treat canonical Risk as authoritative and immutable. It SHALL NOT create,
modify, or replace canonical Risk. Where a derived value differs from canonical Risk, canonical Risk
remains authoritative and the derived value is presented as a presentation-only figure.

---

# Consequences

## Positive

- Rich, presentation-ready risk analysis without disturbing canonical ownership.
- The name reflects the responsibility and preserves Domain ownership of Risk.

## Negative

- Derived figures may differ from canonical Risk; the capability must always mark them as derived.

## Neutral

- Additional scoring frameworks and trend analysis are deferred to future extensions.

---

# Alternatives Considered

- Naming the capability `risk-scoring`. Rejected because it implies ownership of Risk, which belongs
  to Domain Security.
- Allowing Reporting to write canonical Risk. Rejected because canonical Risk is owned by Domain
  Security and is immutable to Reporting.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Risk Schema](../../../../schemas/risk.md)
- [Reporting](../../../shared/reporting/README.md)
