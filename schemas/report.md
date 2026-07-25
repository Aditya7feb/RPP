# Report Schema

**File:** `schemas/report.md`

**Version:** 1.0.0

---

# Purpose

The Report Schema defines the canonical representation of a penetration testing report within the Robust PenTest Platform (RPP).

A Report consolidates the results of an assessment into a structured, traceable, and auditable document suitable for technical teams, security leadership, auditors, and stakeholders.

The schema defines the report structure, not its presentation.

---

# Design Principles

A Report SHALL be

- Evidence-backed
- Traceable
- Reproducible
- Versioned
- Auditable
- Human-readable
- Machine-readable

The Report SHALL reference assessment objects rather than duplicate them.

---

# Relationship

```
Assessment
    │
    ├── Tasks
    │
    ├── Technologies
    │
    ├── Findings
    │
    ├── Evidence
    │
    └── Report
```

---

# Identity

Every Report SHALL contain

```yaml
report_id:

assessment_id:

schema_version:
```

---

# Metadata

Every Report SHALL include

```yaml
title:

report_type:

version:

generated_by:

generated_at:
```

---

# Supported Report Types

```
Executive

Technical

Compliance

Validation

Assessment Summary

Internal

Custom
```

---

# Assessment Reference

Every Report SHALL reference

```yaml
assessment:

assessment_name:

assessment_type:
```

---

# Executive Summary

The Report SHOULD include

```yaml
executive_summary:

overview:

overall_risk:

key_observations:

business_impact:
```

The Executive Summary SHOULD be understandable by non-technical stakeholders.

---

# Scope

The Report SHALL define

```yaml
scope:

targets:

included_assets:

excluded_assets:

rules_of_engagement:
```

---

# Methodology

The Report SHALL describe

```yaml
methodology:

frameworks:

tools:

techniques:
```

Examples

- PTES
- OWASP Testing Guide
- NIST SP 800-115
- Internal Methodology

---

# Technology Inventory

The Report MAY reference

```yaml
technologies:

- technology_id
```

The Report SHALL NOT duplicate Technology definitions.

---

# Findings

The Report SHALL reference

```yaml
findings:

- finding_id
```

Findings SHALL be ordered according to the reporting strategy.

---

# Finding Summary

The Report SHOULD summarize

```yaml
summary:

critical:

high:

medium:

low:

informational:
```

---

# Risk Summary

The Report SHOULD include

```yaml
risk:

overall_score:

critical_assets:

highest_severity:

accepted_risks:
```

---

# Evidence References

Evidence SHALL be referenced.

```yaml
evidence:

- evidence_id
```

Evidence SHALL NOT be embedded unless required by the output format.

---

# Recommendations

The Report SHOULD provide

```yaml
recommendations:

immediate:

short_term:

long_term:
```

Recommendations SHOULD prioritize root-cause remediation.

---

# Assessment Metrics

The Report MAY summarize

```yaml
metrics:

hosts_assessed:

services_identified:

technologies_detected:

tasks_completed:

duration:
```

---

# Limitations

The Report SHOULD document

```yaml
limitations:

constraints:

assumptions:
```

Examples

- Limited testing window
- Network restrictions
- Missing credentials
- Customer exclusions

---

# Appendices

The Report MAY include

```yaml
appendices:

tool_versions:

command_history:

artifacts:

references:
```

---

# Compliance Mapping

Reports MAY reference

```yaml
compliance:

pci_dss:

iso_27001:

nist:

soc2:

custom:
```

---

# Report Status

Supported values

```
Draft

Review

Approved

Published

Archived
```

---

# Review Information

Reports MAY include

```yaml
reviewed_by:

reviewed_at:

approved_by:
```

---

# Distribution

Reports MAY define

```yaml
classification:

audience:

distribution:
```

Example classifications

```
Public

Internal

Confidential

Restricted
```

---

# Audit Metadata

Every Report SHALL record

```yaml
created_at:

updated_at:

revision:

change_history:
```

---

# Validation Rules

A valid Report SHALL contain

- Report ID
- Assessment ID
- Metadata
- Scope
- Methodology
- Findings Reference
- Report Status
- Schema Version

---

# Quality Requirements

A Report SHALL

✓ Reference Findings

✓ Reference Evidence

✓ Reference Technologies

✓ Include Executive Summary

✓ Include Scope

✓ Include Methodology

✓ Preserve traceability

✓ Support auditability

---

# Future Extensions

Future versions MAY include

- CVSS aggregation
- EPSS integration
- MITRE ATT&CK mapping
- Risk trend analysis
- Historical comparison
- AI-generated executive summaries
- Multi-language reporting

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Report provides a complete, traceable, and evidence-backed representation of an assessment.

It SHALL serve as the authoritative deliverable for communicating assessment results to technical teams, leadership, auditors, and other stakeholders while preserving links to the underlying Assessment, Tasks, Findings, Technologies, and Evidence.