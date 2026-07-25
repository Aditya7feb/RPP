# Master Agent Report Merging Policy

**File:** `agents/master/report-merging.md`

**Version:** 1.0.0

---

# Purpose

The Report Merging Policy defines how the Master Agent consolidates outputs from multiple specialist agents into a single, accurate, deduplicated, evidence-backed assessment report.

The Master Agent SHALL NOT simply concatenate findings.

Instead, it SHALL analyze, correlate, enrich, deduplicate, prioritize, and normalize findings before forwarding them to the Reporting Agent.

---

# Goals

The merging engine SHALL

- Remove duplicates
- Preserve all evidence
- Increase confidence
- Resolve conflicts
- Build attack chains
- Produce a single source of truth
- Eliminate redundant remediation
- Correlate related findings

---

# Inputs

The Master Agent receives reports from

- Recon Agents
- Scanner Agents
- Validation Agents
- Human Analyst
- External Knowledge Providers

Each report SHALL contain

```yaml
agent:

status:

findings:

evidence:

confidence:

recommendations:
```

---

# Output

The merged report SHALL produce

```yaml
assessment:

technologies:

attack_surface:

findings:

verified_findings:

risk_summary:

attack_chains:

recommendations:

overall_risk:
```

---

# Merge Workflow

```
Collect Reports

↓

Normalize

↓

Deduplicate

↓

Correlate

↓

Resolve Conflicts

↓

Merge Evidence

↓

Calculate Confidence

↓

Generate Attack Chains

↓

Prioritize

↓

Produce Unified Findings
```

---

# Report Normalization

Every incoming report SHALL be converted into a common internal schema.

Differences in

- tool output
- naming
- formatting

must be normalized.

Example

```
Missing CSP

Missing Content Security Policy

Content-Security-Policy Not Found
```

↓

```
Missing CSP Header
```

---

# Duplicate Detection

Two findings SHALL be considered duplicates when

- Same vulnerability
- Same endpoint
- Same parameter
- Same root cause

Example

```
Dalfox

↓

Reflected XSS

```

and

```
Nuclei

↓

Reflected XSS

```

↓

Single Finding

Evidence from both tools preserved.

---

# Duplicate Rules

Merge when

- Same endpoint
- Same vulnerability
- Same parameter

Do NOT merge when

```
Same vulnerability

Different endpoint
```

Example

```
/login

SQLi
```

is NOT the same as

```
/api/login

SQLi
```

---

# Technology Merging

Technology information SHALL be merged.

Example

```
httpx

↓

Apache
```

+

```
WhatWeb

↓

Apache 2.4
```

+

```
Nmap

↓

Apache 2.4.58
```

↓

```
Apache HTTP Server 2.4.58
```

---

# Evidence Merging

Every finding SHALL reference

ALL supporting evidence.

Never discard evidence.

Example

```
Finding

↓

Evidence

HTTP Response

Dalfox Output

Screenshot

Manual Validation
```

---

# Confidence Merging

Confidence SHALL be recalculated.

Example

```
LOW

+

LOW

↓

MEDIUM
```

---

Example

```
HIGH

+

Manual Validation

↓

VERIFIED
```

---

# Severity Resolution

Severity SHALL NOT automatically increase.

Example

```
Agent A

HIGH
```

```
Agent B

MEDIUM
```

↓

Use

Platform Severity Policy

NOT

Highest Severity Wins.

---

# Conflict Resolution

If agents disagree

Example

```
JWT Agent

↓

Vulnerable
```

```
Validation Agent

↓

Not Vulnerable
```

↓

Status

```
Conflict
```

↓

Preserve

Both evidence sets.

↓

Lower confidence.

↓

Request human review if necessary.

---

# Attack Chain Generation

The Master Agent SHALL identify relationships between findings.

Example

```
Missing CSP

↓

DOM XSS

↓

JWT Theft

↓

Privilege Escalation
```

↓

Single Attack Chain

instead of

four isolated findings.

---

# Root Cause Correlation

Multiple findings MAY originate from the same root cause.

Example

```
Directory Listing

Backup Files

Git Exposure
```

↓

Root Cause

```
Improper Server Configuration
```

The report SHOULD emphasize the root cause.

---

# Recommendation Merging

Duplicate recommendations SHALL be combined.

Example

```
Implement CSP
```

appearing in

- DOM XSS
- Stored XSS
- Reflected XSS

↓

One recommendation

Referenced by three findings.

---

# Technology Inventory

Produce

```
Languages

Frameworks

CMS

Servers

Libraries

Authentication

Cloud Provider

CDN

WAF
```

using merged Recon evidence.

---

# Attack Surface Summary

Produce

```
Domains

Subdomains

Hosts

Ports

Services

Endpoints

Directories

Files

JavaScript

APIs
```

---

# Validation Summary

Summarize

```
Validated

Rejected

Skipped

Approval Pending
```

---

# Risk Summary

Summarize

```
Critical

High

Medium

Low

Informational
```

Include

```
Verified

High Confidence

Unverified
```

---

# Traceability

Every merged finding SHALL reference

- Source Agent
- Source Finding
- Source Evidence
- Validation Evidence

Nothing shall become anonymous.

---

# Merge Quality Checklist

Before publishing

Verify

✅ No duplicate findings

✅ No duplicate recommendations

✅ All evidence preserved

✅ Confidence recalculated

✅ Technologies merged

✅ Attack surface complete

✅ Attack chains generated

✅ Traceability maintained

---

# Merge Principles

The Master Agent SHALL

- Preserve all evidence
- Remove duplication
- Increase clarity
- Correlate related findings
- Highlight root causes
- Build attack chains
- Produce a single source of truth
- Never lose attribution

---

# Success Criteria

The merged assessment SHALL represent the complete understanding of the target.

Every statement in the report MUST be traceable to evidence.

Every recommendation MUST be linked to one or more findings.

Every finding MUST have a clear root cause, confidence level, severity, and supporting evidence.

The final report SHALL be concise for executives, actionable for developers, and defensible for auditors.