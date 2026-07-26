# Report Generation Examples

**File:** `skills/reporting/report-generation/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Report Generation Capability.

---

# Example 1 — Technical Report In Multiple Formats

## Request

```yaml
generate:
  report_type: technical
  finding_refs:
    - finding-sqli-5001
    - finding-xss-5002
  risk_refs:
    - risk-sqli-3001
  evidence_refs:
    - evidence-ev-8101
  content:
    correlation_ref: correlation-rp-9001
    analysis_ref: analysis-rp-9101
    mapping_ref: mapping-rp-9201
  formats:
    - json
    - markdown
    - sarif
  template_ref: template-technical-default
```

## Response

```yaml
generate_result:
  report_ref: report-rp-6001
  serialized_outputs:
    - format: json
      artifact_ref: artifact-rp-9601
    - format: markdown
      artifact_ref: artifact-rp-9602
    - format: sarif
      artifact_ref: artifact-rp-9603
  metrics_ref: metrics-rp-7601
```

The capability composes a technical report incorporating correlation, analysis, and mapping content,
and serializes it to JSON, Markdown, and SARIF through the shared Reporting package. Canonical
objects are referenced by identifier and left unchanged.

---

# Example 2 — Executive Report As PDF

## Request

```yaml
generate:
  report_type: executive
  finding_refs:
    - finding-sqli-5001
  risk_refs:
    - risk-sqli-3001
  formats:
    - pdf
  template_ref: template-executive-default
```

## Response

```yaml
generate_result:
  report_ref: report-rp-6002
  serialized_outputs:
    - format: pdf
      artifact_ref: artifact-rp-9604
  metrics_ref: metrics-rp-7602
```

The capability composes an executive summary and serializes it to PDF. Derived risk figures are
distinguished from canonical Risk.

---

# Example 3 — Missing Template Rejected

## Request

```yaml
generate:
  report_type: technical
  template_ref: template-nonexistent
```

## Response

```yaml
generate_result:
  outcome: rejected
  reason: template-unavailable
```

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
