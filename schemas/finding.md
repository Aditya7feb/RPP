# Finding Schema

**File:** `schemas/finding.md`

**Version:** 1.0.0

---

# Purpose

The Finding Schema defines the canonical representation of a security finding within the Robust PenTest Platform (RPP).

A Finding represents an observed security issue, weakness, misconfiguration, exposure, or informational result discovered during an assessment.

Every reported issue SHALL conform to this schema.

---

# Design Principles

A Finding SHALL be

- Evidence-backed
- Traceable
- Explainable
- Versioned
- Reproducible
- Auditable
- Implementation-independent

A Finding SHALL NEVER exist without supporting evidence.

---

# Relationship

```
Assessment
    │
    ├── Tasks
    │      │
    │      └── Findings
    │               │
    │               └── Evidence
```

---

# Identity

Every Finding SHALL include

```yaml
finding_id:

assessment_id:

task_id:

schema_version:
```

Finding IDs SHALL be unique within an assessment.

---

# Classification

Every Finding SHALL define

```yaml
category:

type:

family:

cwe:

owasp:

cvss:
```

Example

```yaml
category: Injection

type: SQL Injection

family: OWASP Top 10

cwe: CWE-89

owasp: A03:2021

cvss: 9.8
```

---

# Basic Information

Every Finding SHALL contain

```yaml
title:

summary:

description:

impact:
```

Descriptions SHALL explain

- What was found
- Why it matters
- How it affects the target

---

# Severity

Allowed values

```
Critical

High

Medium

Low

Informational
```

Severity measures business impact.

Severity SHALL NOT represent confidence.

---

# Confidence

Allowed values

```
Low

Medium

High

Verified
```

Confidence measures certainty.

Confidence SHALL be calculated according to

```
agents/master/confidence-model.md
```

---

# Status

Allowed values

```
OPEN

VERIFIED

UNVERIFIED

FALSE_POSITIVE

ACCEPTED_RISK

FIXED

DUPLICATE
```

---

# Affected Target

Every Finding SHALL specify

```yaml
target:

host:

endpoint:

parameter:

method:
```

Example

```
POST /api/login

parameter=password
```

---

# Root Cause

Every Finding SHALL identify

```yaml
root_cause:

technical_reason:

security_control_missing:
```

Example

```
Missing Output Encoding
```

---

# Evidence References

Every Finding SHALL reference one or more Evidence objects.

```yaml
evidence:

- evidence_id
- evidence_id
```

Evidence SHALL NOT be duplicated inside the Finding.

---

# Discovery Metadata

Every Finding SHALL record

```yaml
discovered_by:

discovered_at:

agent:

tool:
```

---

# Validation

Validation information

```yaml
validated:

validated_by:

validated_at:

approval_reference:
```

Validation SHALL remain optional.

---

# Exploitability

Each Finding SHOULD describe

```yaml
attack_complexity:

privileges_required:

user_interaction:

authentication_required:
```

These values SHOULD align with industry standards where applicable.

---

# Business Impact

Every Finding SHOULD include

```yaml
confidentiality:

integrity:

availability:

business_risk:
```

---

# Remediation

Each Finding SHALL include

```yaml
recommendation:

remediation_steps:

references:
```

Recommendations SHALL describe the root cause rather than only the observed symptom whenever possible.

---

# Tags

Findings MAY contain

```yaml
tags:

- xss
- reflected
- authentication
- jwt
```

Tags improve searching and reporting.

---

# Relationships

Findings MAY reference

```yaml
related_findings:

duplicate_of:

parent_finding:

child_findings:
```

This supports attack chain construction.

---

# Attack Chain

A Finding MAY belong to

```yaml
attack_chain:

stage:

prerequisites:
```

Example

```
Information Disclosure

↓

Credential Theft

↓

Privilege Escalation
```

---

# References

Findings MAY reference

- CWE
- CAPEC
- OWASP
- CVE
- Vendor Advisories
- Internal Knowledge Base

---

# Lifecycle

```
Discovered

↓

Confirmed

↓

Validated

↓

Reported

↓

Resolved

↓

Closed
```

Alternative path

```
Discovered

↓

False Positive
```

---

# Quality Requirements

A Finding SHALL

✓ Have evidence

✓ Have severity

✓ Have confidence

✓ Have affected target

✓ Have remediation

✓ Have traceability

✓ Have discovery metadata

---

# Validation Rules

A valid Finding SHALL contain

- Finding ID
- Assessment ID
- Task ID
- Title
- Severity
- Confidence
- At least one Evidence reference
- Discovery metadata

---

# Future Extensions

Future versions MAY include

- MITRE ATT&CK mappings
- Compliance mappings
- EPSS score
- Asset criticality
- Risk acceptance workflow
- AI-generated remediation

Backward compatibility SHOULD be preserved.

---

# Success Criteria

A compliant Finding represents a complete, evidence-backed description of a security issue.

Every Finding SHALL be reproducible, traceable, explainable, and independently verifiable through its associated Evidence.