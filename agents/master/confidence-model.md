# Master Agent Confidence Model

**File:** `agents/master/confidence-model.md`

**Version:** 1.0.0

---

# Purpose

The Confidence Model defines how the Master Agent evaluates the trustworthiness of findings returned by specialist agents.

Confidence SHALL represent the likelihood that a reported finding accurately reflects the target's security posture.

Confidence is NOT severity.

Confidence measures certainty.

Severity measures impact.

---

# Guiding Principle

Confidence SHALL be determined from evidence.

Never from assumptions.

Never from guesses.

Never from tool reputation.

---

# Confidence Levels

The platform supports four confidence levels.

```
LOW

MEDIUM

HIGH

VERIFIED
```

---

# LOW Confidence

Requirements

- Single indicator
- Weak evidence
- No corroboration
- Automated inference

Examples

- Technology guessed from headers
- Possible admin panel
- Possible SQL Injection
- Interesting response difference

LOW confidence findings SHALL NOT trigger validation.

---

# MEDIUM Confidence

Requirements

- Multiple indicators
- Same tool
- Partial confirmation
- Some supporting evidence

Examples

- Nuclei identifies XSS
- Response contains payload reflection
- Security headers missing
- CMS version detected

MEDIUM findings MAY trigger additional scanners.

---

# HIGH Confidence

Requirements

- Independent agreement
- Strong evidence
- Multiple tools
- Clear indicators

Examples

```
Dalfox

+

Nuclei

↓

XSS
```

---

Example

```
httpx

+

WhatWeb

+

Wappalyzer

↓

Technology Detection
```

HIGH confidence findings MAY request human approval.

---

# VERIFIED

Requirements

Human-approved

AND

Read-only validation successful.

Examples

```
SQLMap

↓

Approval

↓

Validation

↓

Verified SQL Injection
```

OR

```
JWT validation

↓

Server accepts alg=none

↓

Verified
```

VERIFIED findings SHALL always include proof.

---

# Confidence Calculation

Confidence SHALL consider

- Evidence quality
- Number of tools
- Independent confirmation
- Manual validation
- Response consistency
- False positive probability

---

# Confidence Factors

Every finding SHALL include

```yaml
confidence:

evidence_count:

tool_count:

manual_validation:

independent_confirmation:

false_positive_probability:
```

---

# Evidence Weight

Different evidence contributes differently.

Example

```
HTTP Response

Weight = High
```

---

Example

```
Screenshot

Weight = Medium
```

---

Example

```
Tool Warning

Weight = Low
```

---

Example

```
Validated Request/Response Pair

Weight = Very High
```

---

# Tool Independence

Independent tools increase confidence.

Example

```
Nuclei

+

Dalfox

↓

Independent

↓

Higher Confidence
```

---

Example

```
Nuclei

+

Another Nuclei Template

↓

NOT Independent
```

Confidence increase should be smaller.

---

# Manual Validation

Manual validation always increases confidence.

Example

```
Automated Scanner

↓

HIGH

↓

Manual Validation

↓

VERIFIED
```

---

# False Positive Reduction

Confidence SHALL decrease when

- Tool disagreement
- Inconsistent responses
- WAF interference
- Missing evidence
- Unstable behaviour

---

# False Negative Awareness

Absence of findings

DOES NOT

prove absence of vulnerabilities.

The Master Agent SHALL distinguish

```
No Evidence

≠

Evidence of No Issue
```

---

# Confidence Adjustment

Confidence SHALL increase when

- Multiple independent scanners agree
- Manual validation succeeds
- Repeatable behaviour observed
- Strong evidence collected

Confidence SHALL decrease when

- Behaviour inconsistent
- Response unstable
- WAF interference detected
- Scanner disagreement
- Weak evidence

---

# Severity Independence

Confidence SHALL NEVER affect severity.

Example

```
Critical

LOW Confidence
```

is possible.

Example

```
Low Severity

VERIFIED
```

is also possible.

---

# Reporting Rules

Reports SHALL always include

```
Severity

Confidence
```

as separate fields.

Example

```
Severity

HIGH

Confidence

MEDIUM
```

---

# Validation Threshold

Default policy

```
LOW

↓

Do Nothing
```

```
MEDIUM

↓

Collect More Evidence
```

```
HIGH

↓

Eligible for Approval
```

```
VERIFIED

↓

Final Report
```

---

# Conflicting Evidence

When specialists disagree

The Master Agent SHALL

- Preserve both findings
- Lower confidence
- Schedule another specialist if justified

Never discard evidence automatically.

---

# Confidence Lifecycle

```
Discovery

↓

Evidence

↓

Correlation

↓

Independent Confirmation

↓

Human Approval

↓

Validation

↓

VERIFIED
```

---

# Confidence Metadata

Every finding SHALL include

```yaml
confidence:

confidence_reason:

supporting_agents:

supporting_tools:

evidence_count:

last_updated:
```

---

# Confidence Principles

The Master Agent SHALL

- Trust evidence over assumptions
- Prefer independent confirmation
- Encourage validation
- Preserve uncertainty
- Never exaggerate confidence
- Explain confidence decisions
- Continuously recalculate confidence as new evidence arrives

---

# Success Criteria

A confidence assessment is considered complete when

- Evidence has been evaluated
- Independent confirmations identified
- Confidence level assigned
- Confidence reasoning documented
- Findings eligible for reporting or validation have been correctly classified