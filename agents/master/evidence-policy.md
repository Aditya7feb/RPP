# Master Agent Evidence Policy

**File:** `agents/master/evidence-policy.md`

**Version:** 1.0.0

---

# Purpose

The Evidence Policy defines how evidence is collected, preserved, validated, correlated, and stored throughout the assessment lifecycle.

Every reported finding MUST be backed by evidence.

Findings without evidence SHALL NOT appear in the final report.

---

# Guiding Principles

Evidence SHALL be

- Accurate
- Immutable
- Traceable
- Reproducible
- Timestamped
- Explainable

The platform SHALL always report evidence.

Never opinions.

Never assumptions.

Never guesses.

---

# Evidence Definition

Evidence is any artifact that supports or disproves a security finding.

Examples include

- HTTP Requests
- HTTP Responses
- Screenshots
- Response Headers
- TLS Certificates
- Tool Output
- Terminal Output
- API Responses
- Logs
- Stack Traces
- JavaScript Files
- Configuration Files
- Metadata

---

# Evidence Sources

Evidence MAY originate from

- Recon Agents
- Scanner Agents
- Validation Agents
- Human Analyst
- Customer Provided Data

Every evidence item MUST identify its source.

---

# Evidence Categories

The platform supports the following evidence categories.

```
NETWORK

APPLICATION

TLS

DNS

HTTP

SCREENSHOT

LOG

FILE

TOOL_OUTPUT

MANUAL_VALIDATION

CONFIGURATION

METADATA
```

---

# Evidence Ownership

Every evidence object SHALL have exactly one owner.

The owner SHALL be the agent that collected it.

Example

```
Evidence

↓

Collected by

↓

TLS Agent
```

Ownership SHALL NOT change.

---

# Required Metadata

Every evidence object MUST include

```yaml
evidence_id:

assessment_id:

task_id:

agent:

tool:

timestamp:

category:

source:

target:

confidence:

hash:
```

---

# Evidence Integrity

Evidence SHALL NEVER be modified after collection.

If processing is required

Create

Derived Evidence

instead.

Original evidence SHALL remain unchanged.

---

# Derived Evidence

Derived Evidence is created by processing existing evidence.

Examples

Original

```
HTTP Response
```

↓

Extract

```
JWT Token
```

↓

Derived Evidence

Another example

```
JavaScript File

↓

Extract Secrets

↓

Derived Evidence
```

Original artifacts SHALL always be preserved.

---

# Evidence Hashing

Every evidence object SHOULD include

```
SHA-256
```

or stronger hashing.

Purpose

- Integrity
- Deduplication
- Auditability

---

# Evidence Correlation

Multiple evidence objects MAY support a single finding.

Example

```
Nuclei Output

+

HTTP Response

+

Screenshot

↓

Single Finding
```

Correlation SHALL preserve links to every supporting artifact.

---

# Evidence Confidence

Evidence SHALL have its own confidence.

Evidence confidence contributes to finding confidence.

Example

```
HTTP Request/Response

HIGH
```

```
Screenshot

MEDIUM
```

```
Tool Warning

LOW
```

---

# Evidence Lifecycle

```
Collect

↓

Validate

↓

Normalize

↓

Hash

↓

Store

↓

Correlate

↓

Reference

↓

Archive
```

Evidence SHALL never bypass lifecycle stages.

---

# Duplicate Evidence

Duplicate evidence SHALL NOT be stored twice.

Duplicate detection SHOULD use

- Hash
- Size
- Source
- Timestamp
- Content Similarity

Instead

Reference existing evidence.

---

# Evidence Validation

Before accepting evidence verify

- Complete
- Readable
- Relevant
- Within Scope
- Timestamped
- Source Known
- Hash Valid

Invalid evidence SHALL be rejected.

---

# Required Evidence Per Finding

Every finding MUST include

- Primary Evidence
- Supporting Evidence
- Collection Timestamp
- Source Agent
- Collection Tool
- Confidence

Findings lacking evidence SHALL remain

```
UNSUPPORTED
```

and SHALL NOT appear in the final report.

---

# Request / Response Preservation

For HTTP findings preserve

Request

- Method
- URL
- Headers
- Parameters
- Cookies
- Body

Response

- Status Code
- Headers
- Body
- Response Time

Sensitive values SHALL be redacted.

---

# Screenshot Policy

Screenshots SHOULD be collected

When

- Visual confirmation improves understanding
- Authentication state matters
- UI behaviour demonstrates impact

Screenshots SHALL NOT replace HTTP evidence.

---

# Sensitive Data Handling

Evidence MAY contain

- Tokens
- Cookies
- JWTs
- API Keys
- Credentials
- Personal Data

Sensitive values SHALL be

- Masked
- Redacted
- Encrypted when stored

The original value SHALL NOT appear in reports unless explicitly required.

---

# Tool Output

Raw tool output SHALL always be preserved.

Processed findings SHALL reference

Raw Output

rather than replacing it.

---

# Manual Validation Evidence

Human validation SHALL include

- Steps Performed
- Expected Behaviour
- Actual Behaviour
- Requests
- Responses
- Screenshots (optional)
- Analyst Notes

Manual evidence SHALL receive the highest confidence weighting.

---

# Chain of Custody

Evidence SHALL maintain

```
Collected By

↓

Processed By

↓

Referenced By

↓

Reported By
```

Every transition SHALL be auditable.

---

# Evidence Storage Structure

Recommended hierarchy

```
Assessment

↓

Agent

↓

Task

↓

Evidence
```

Example

```
Assessment

    Recon

        DNS

            dns-output.json

        TLS

            certificate.pem

    Scanner

        JWT

            response.json

        XSS

            request.txt

            response.txt

            screenshot.png
```

---

# Evidence Retention

Evidence SHALL remain available until

- Assessment completed
- Report finalized
- Audit period expired

Evidence SHALL NOT be deleted during an active assessment.

---

# Evidence in Reports

Reports SHALL reference

Evidence IDs

rather than embedding large artifacts.

Example

```
Finding

↓

Evidence

EVD-000431

EVD-000512

EVD-000519
```

---

# Quality Requirements

Evidence SHALL be

✓ Relevant

✓ Complete

✓ Repeatable

✓ Timestamped

✓ Traceable

✓ Immutable

✓ Understandable

---

# Common Evidence Mistakes

Avoid

- Missing HTTP responses
- Missing timestamps
- Missing tool names
- Screenshots without requests
- Requests without responses
- Unmasked secrets
- Modified evidence
- Duplicate artifacts

---

# Success Criteria

The evidence model is considered successful when

- Every finding references evidence
- Evidence integrity is preserved
- Evidence is reproducible
- Evidence supports confidence calculations
- Reports can trace every conclusion back to original artifacts

---

# Guiding Principles

The Master Agent SHALL

- Preserve every artifact
- Never modify original evidence
- Correlate related evidence
- Eliminate duplicate artifacts
- Protect sensitive information
- Ensure complete traceability
- Build every conclusion on verifiable evidence

The credibility of the entire assessment depends on the quality of its evidence.