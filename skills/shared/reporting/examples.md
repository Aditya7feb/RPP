# Reporting Examples

**File:** `skills/shared/reporting/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Reporting Shared Skill in use.

Examples demonstrate consumers, aggregation, deduplication, correlation,
ordering, evidence bundling, rendering, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Composing A Report

The Master Agent composes a report from aggregated findings.

## Compose Request

```yaml
metadata:
  request_id: req-9001
  assessment_id: asmt-42
findings: collection://asmt-42/findings
deduplicate: true
correlate: true
order_by: severity_then_confidence
include_evidence: true
formats:
  - json
  - markdown
```

## Result

```yaml
outcome: composed
report_ref: report-asmt-42
rendered:
  json: render://report-asmt-42.json
  markdown: render://report-asmt-42.md
metrics:
  findings_in: 47
  duplicates_merged: 6
  correlations: 4
```

The canonical report is composed and rendered into JSON and Markdown.

---

# Example 2 — Deduplication Merges Evidence

Two skills report the same issue at the same location.

## Before

```
finding-xss-0007 (confidence: 0.8, evidence: [ev-1])
finding-xss-0012 (confidence: 0.6, evidence: [ev-2])
```

## After Deduplication

```yaml
finding: finding-xss-0007
confidence: 0.8
evidence:
  - ev-1
  - ev-2
```

The retained finding keeps the higher confidence and merges evidence references.

---

# Example 3 — Correlation Grouping

Multiple injection points of one class are correlated.

## Correlation

```yaml
correlation:
  id: corr-sqli-01
  class: sql-injection
  findings:
    - finding-sqli-0003
    - finding-sqli-0004
    - finding-sqli-0009
```

Individual finding validity is unchanged; correlation aids presentation.

---

# Example 4 — Severity Ordering

Findings are ordered by severity, then confidence, with a stable tie-breaker.

## Ordered Output

```
1. critical / 0.95 / finding-rce-0001
2. high / 0.90 / finding-sqli-0003
3. high / 0.75 / finding-idor-0011
4. medium / 0.80 / finding-xss-0007
```

Ordering is deterministic across runs.

---

# Example 5 — Evidence Bundling Preserves Redaction

Bundled evidence retains its redaction and integrity.

## Bundled Evidence Reference

```yaml
evidence:
  - evidence_ref: evidence-http-4002
    integrity:
      verified: true
    redaction:
      applied: true
```

Rendered output references the evidence and never exposes redacted values.

---

# Example 6 — Partial Render

The PDF renderer fails while JSON succeeds.

## Result

```yaml
outcome: partial
report_ref: report-asmt-42
rendered:
  json: render://report-asmt-42.json
errors:
  - format: pdf
    category: Rendering
    code: render_failed
    retryable: true
```

The canonical report is preserved; only the PDF format failed and MAY be
retried.

---

# Example 7 — Canonical Report Reference Traceability

A rendered report traces every finding to evidence.

```
report-asmt-42
  ├── finding-rce-0001 → evidence-cmd-0001
  ├── finding-sqli-0003 → evidence-sql-0003
  └── finding-xss-0007 → [ evidence-http-4002, evidence-dom-0007 ]
```

Traceability is preserved from report to evidence through references.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Report Schema](../../../schemas/report.md)
- [Finding Schema](../../../schemas/finding.md)
- [Evidence](../evidence/README.md)
