# ADR-001 — Reporting Abstraction

**File:** `skills/shared/reporting/adr/ADR-001-reporting-abstraction.md`

**Status:** Accepted

**Version:** 1.0.0

---

# Context

The value of an assessment is realized through its report. Reporting aggregates
findings from many domain skills, correlates related issues, bundles supporting
evidence, and renders output for different audiences. Reporting carries several
requirements:

- Deterministic, reproducible composition
- Traceability from every reported item to evidence
- Preservation of evidence integrity and redaction in output
- Consistent deduplication and correlation
- Multiple output formats for different audiences

Before this decision, report assembly could be implemented ad hoc per workflow.
That approach produced inconsistent structure, non-deterministic ordering, risk
of exposing redacted material, and duplicated evidence.

The platform requires a single, canonical, implementation-independent mechanism
to compose and render reports.

---

# Decision

The platform SHALL provide a dedicated Reporting shared skill that centralizes
report composition and rendering behind a stable interface.

The Reporting shared skill SHALL

- Aggregate canonical [Findings](../../../../schemas/finding.md)
- Deduplicate and correlate related findings
- Order findings deterministically by declared severity and confidence
- Bundle referenced evidence through the
  [Evidence](../../evidence/README.md) shared package, preserving integrity and
  redaction
- Compose a canonical [Report](../../../../schemas/report.md) independent of
  format
- Render the report into requested formats through adapters

Consumers SHALL compose reports exclusively through the
[Reporting Interface](../interface.md). Renderer implementations SHALL remain
hidden behind adapters. Reporting SHALL NOT produce findings or reinterpret
their validity.

---

# Alternatives Considered

## Ad Hoc Report Assembly Per Workflow

Each workflow could assemble its own report.

Rejected because it produces inconsistent structure, non-deterministic ordering,
and risk of exposing redacted material, with duplicated evidence.

## Findings Rendered Directly Without A Canonical Model

Skills could render findings directly.

Rejected because a format-independent canonical report model is required to
support multiple output formats consistently and to preserve traceability.

## Embedding Evidence In Reports

Evidence could be embedded inline in reports.

Rejected because it duplicates large payloads, risks exposing redacted material,
and breaks the single-source integrity guarantee of the Evidence shared
package. Reference-based bundling is superior.

---

# Consequences

## Positive

- Deterministic, reproducible reports across runs
- Consistent deduplication, correlation, and ordering
- Traceability from report to evidence preserved
- Evidence integrity and redaction preserved in output
- Multiple output formats through a single canonical model

## Negative

- Consumers MUST compose reports through the interface
- An additional shared dependency is introduced
- Format renderers must be maintained as adapters

The negative consequences are outweighed by the consistency, safety, and
traceability benefits.

---

# Compliance

Consumers SHALL

- Submit findings conforming to the Finding schema
- Reference evidence rather than embedding it
- Rely on deduplication, correlation, and deterministic ordering
- Never expose redacted material in output

Reporting SHALL depend on the Evidence shared skill and the canonical schemas,
and SHALL NOT depend on domain skills.

---

# Future Compatibility

Future versions MAY introduce delta reporting, template descriptors, and
standards enrichment such as OWASP and MITRE ATT&CK mappings. These extensions
SHALL preserve the existing interface and SHALL maintain backward compatibility.

---

# Related Documents

- [Reporting README](../README.md)
- [Reporting Interface](../interface.md)
- [Reporting Execution Model](../execution.md)
- [Reporting Error Model](../error-model.md)
- [Report Schema](../../../../schemas/report.md)
- [Finding Schema](../../../../schemas/finding.md)
- [Evidence](../../evidence/README.md)
