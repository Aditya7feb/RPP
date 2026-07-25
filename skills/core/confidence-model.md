# Skill Confidence Model

**File:** `skills/core/confidence-model.md`

**Version:** 1.0.0

---

# Purpose

The Skill Confidence Model defines how skills measure, calculate, report, and propagate confidence throughout the Robust PenTest Platform (RPP).

Confidence represents the platform's certainty that an observation, technology, evidence item, or finding is correct.

Confidence SHALL be independent of severity.

---

# Design Principles

Confidence SHALL be

- Evidence-based
- Explainable
- Reproducible
- Composable
- Auditable
- Deterministic
- Implementation Independent

Every reported confidence value SHALL be explainable.

---

# Relationship

```
Skill

↓

Observation

↓

Evidence

↓

Confidence

↓

Finding

↓

Report
```

Confidence SHALL propagate through every stage of assessment.

---

# Confidence vs Severity

These concepts SHALL remain independent.

Example

```
SQL Injection

Confidence

Verified

Severity

Critical
```

Another example

```
Possible SQL Injection

Confidence

Low

Severity

Critical
```

The business impact remains critical even if confidence is low.

---

# Confidence Levels

Supported values

```
Unknown

Low

Medium

High

Verified
```

Definitions

## Unknown

Insufficient evidence exists.

Further investigation is required.

---

## Low

Weak indication.

Examples

- Single heuristic
- Partial fingerprint
- Incomplete response
- Unverified observation

---

## Medium

Reasonable indication.

Examples

- Multiple indicators
- Consistent fingerprint
- Partial validation
- Expected behavior observed

---

## High

Strong supporting evidence.

Examples

- Multiple independent observations
- Reproducible behavior
- Reliable tooling
- Manual review

---

## Verified

Confirmed through direct validation.

Examples

- Successful exploitation within scope
- Manual confirmation
- Cryptographic validation
- Multiple independent confirmations

---

# Confidence Sources

Confidence MAY be derived from

- Evidence Quality
- Evidence Quantity
- Multiple Skills
- Multiple Tools
- Manual Validation
- Historical Observations
- Protocol Guarantees
- Target Behavior

Each source SHOULD contribute independently.

---

# Confidence Factors

Skills SHOULD evaluate

```yaml
evidence_quality:

evidence_quantity:

reproducibility:

tool_reliability:

manual_validation:

protocol_guarantees:

corroboration:
```

---

# Evidence Quality

Evidence SHOULD be classified.

Examples

High Quality

- TLS Certificate
- HTTP Response
- Packet Capture
- Screenshot
- API Response

Lower Quality

- Banner Guess
- HTML Comment
- Response Timing
- Error Message

---

# Corroboration

Confidence SHOULD increase when observations agree.

Example

```
HTTP Headers

↓

Nuclei

↓

JavaScript Analysis

↓

Technology Detection
```

Independent corroboration SHOULD improve confidence.

---

# Manual Validation

Manual review MAY increase confidence.

Example

```
Automated Finding

↓

Security Analyst Review

↓

Verified
```

Manual validation SHALL be auditable.

---

# Reproducibility

Confidence SHOULD increase when observations can be reproduced.

Examples

```
Run Once

↓

Medium
```

```
Run Five Times

↓

High
```

Consistent results improve confidence.

---

# Protocol Guarantees

Some protocols provide intrinsic confidence.

Examples

```
TLS Certificate

↓

Verified
```

```
JWT Signature Validation

↓

Verified
```

Cryptographic verification SHOULD produce the highest confidence where appropriate.

---

# Negative Confidence

A skill MAY reduce confidence when

- Conflicting evidence exists
- Target behavior changes
- Responses become inconsistent
- Validation fails

Reduced confidence SHALL include an explanation.

---

# Confidence Propagation

Confidence SHALL propagate.

Example

```
Evidence

↓

Technology

↓

Finding

↓

Report
```

Derived confidence SHALL never exceed the confidence of its strongest supporting evidence without additional justification.

---

# Confidence Aggregation

When multiple observations exist

The platform SHOULD aggregate confidence using

- Independent corroboration
- Manual validation
- Evidence diversity
- Reproducibility

Aggregation SHOULD avoid double-counting identical evidence.

---

# Confidence Decay

Confidence MAY decrease over time.

Examples

- Technology fingerprint several months old
- Cached DNS information
- Historical screenshots

Implementations MAY apply decay policies.

---

# Confidence Overrides

Human analysts MAY override confidence.

Overrides SHALL record

```yaml
previous_value:

new_value:

reviewer:

timestamp:

reason:
```

Overrides SHALL be auditable.

---

# Reporting

Every reported confidence SHALL include

```yaml
level:

reason:

supporting_evidence:

validated_by:
```

Confidence SHALL always be explainable.

---

# Confidence Events

Confidence changes SHOULD generate events.

Examples

- Increased
- Decreased
- Verified
- Invalidated

These events SHOULD update the Execution State.

---

# Validation Rules

A compliant confidence assessment SHALL

- Define a confidence level
- Reference supporting evidence
- Explain the reasoning
- Support auditing
- Support overrides

---

# Quality Requirements

The confidence model SHALL

✓ Remain independent of severity

✓ Be evidence-based

✓ Support corroboration

✓ Support manual validation

✓ Support propagation

✓ Remain explainable

✓ Preserve auditability

✓ Support deterministic reasoning

---

# Future Extensions

Future versions MAY include

- Bayesian confidence models
- Statistical confidence scoring
- Machine learning assisted confidence
- Historical confidence trends
- Confidence calibration
- Confidence benchmarking

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Confidence Model provides a consistent and explainable method for expressing certainty across observations, evidence, technologies, and findings.

It enables the Robust PenTest Platform to make informed planning, validation, and reporting decisions while maintaining transparency, reproducibility, and trust in assessment results.