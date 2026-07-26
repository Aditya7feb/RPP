# ADR-001 — Finding Mapping Capability

**File:** `skills/reporting/finding-mapping/adr/ADR-001-finding-mapping-capability.md`

**Version:** 1.0.0

---

# Status

Accepted

---

# Context

Reports benefit from mapping Findings to recognized frameworks — OWASP categories and MITRE ATT&CK
techniques — for stakeholder communication and coverage summaries. OWASP mapping and MITRE ATT&CK
mapping are the same enrichment concern applied to two frameworks; modeling them as separate packages
would fragment a single capability by framework. Mapping is a Reporting-tier enrichment concern that
must remain read-only and must not alter canonical Finding classification.

---

# Decision

We SHALL provide a Finding Mapping Capability in the Reporting tier that consolidates OWASP and MITRE
ATT&CK mapping. It loads referenced [Findings](../../../../schemas/finding.md); maps them to OWASP
categories and MITRE ATT&CK techniques for presentation, referencing existing classification such as
CWE without altering it; produces mapping content for a [Report](../../../../schemas/report.md)
through the shared [Reporting](../../../shared/reporting/README.md) package; and emits
[Metrics](../../../../schemas/metrics.md). It produces no Findings or Risk and modifies no canonical
objects.

---

# Consequences

## Positive

- One mapping capability spanning frameworks rather than per-framework packages.
- Presentation enrichment that preserves canonical classification and ownership.

## Negative

- Mapping quality depends on Finding attribute completeness.

## Neutral

- Additional frameworks and compliance-control mappings are deferred to future extensions.

---

# Alternatives Considered

- Separate OWASP Mapping and MITRE ATT&CK Mapping packages. Rejected as framework-only fragmentation.
- Writing mappings back onto Findings. Rejected because Findings are immutable and owned by Domain
  Security; mappings are presentation enrichment.

---

# Related Documents

- [README.md](../README.md)
- [capabilities.md](../capabilities.md)
- [interface.md](../interface.md)
- [Finding Schema](../../../../schemas/finding.md)
- [Reporting](../../../shared/reporting/README.md)
