# Master Agent Approval Policy

**File:** `agents/master/approval-policy.md`

**Version:** 1.0.0

---

# Purpose

The Approval Policy defines when the Master Agent MUST pause an assessment and obtain explicit human authorization before continuing.

The objective is to ensure that potentially intrusive, state-changing, or high-risk actions are never executed automatically.

Approval requirements apply regardless of confidence level.

---

# Guiding Principle

The platform SHALL always prefer safety over automation.

No agent may bypass an approval gate.

---

# Approval Workflow

```
Potential Validation Identified

↓

Evaluate Approval Policy

↓

Approval Required?

↓

YES

↓

Create Approval Request

↓

Pause Task

↓

Wait

↓

Approved?

↓

YES

↓

Dispatch Validation Agent

↓

Collect Evidence

↓

Continue Assessment
```

---

# Approval States

Every approval request SHALL exist in one of the following states.

```
NOT_REQUIRED

PENDING

APPROVED

REJECTED

EXPIRED

CANCELLED
```

---

# Actions That Require Approval

The following activities SHALL always require approval.

## Authentication

- Login bypass validation
- Session manipulation
- Account takeover validation
- Password reset abuse
- MFA bypass validation

---

## Injection

- SQL Injection validation
- NoSQL Injection validation
- Command Injection validation
- LDAP Injection validation
- SSTI validation
- XXE validation

---

## Authorization

- IDOR validation
- Horizontal privilege escalation
- Vertical privilege escalation

---

## File Handling

- File Upload validation
- Path Traversal validation
- LFI validation
- RFI validation

---

## Server Interaction

- SSRF validation
- Deserialization validation
- Request Smuggling validation

---

## Business Logic

- Payment manipulation
- Coupon abuse
- Workflow abuse
- Inventory manipulation

---

# Actions That Do NOT Require Approval

The following are considered safe.

- DNS Enumeration
- Port Scanning
- TLS Inspection
- HTTP Fingerprinting
- Header Analysis
- Content Discovery
- robots.txt retrieval
- sitemap.xml retrieval
- Public JavaScript download
- Passive Technology Detection
- Security Header Inspection
- Certificate Analysis

---

# Read-Only Validation

Validation agents SHALL perform only the minimum actions necessary to confirm a finding.

Validation SHALL NOT

- Modify data
- Delete data
- Create users
- Reset passwords
- Change configuration
- Execute persistent payloads
- Upload web shells
- Deploy malware
- Perform denial-of-service

---

# Approval Request

Every approval request SHALL include

```yaml
assessment_id:

task_id:

agent:

finding:

severity:

confidence:

risk:

expected_requests:

expected_duration:

estimated_impact:

rollback_required:

reason:
```

---

# Human Decision

A human reviewer may

```
Approve

Reject

Request More Information

Cancel Assessment
```

---

# Approval Rules

Approval SHALL be explicit.

Silence SHALL NOT be interpreted as approval.

Expired approvals SHALL be treated as rejected.

---

# Scope Validation

Before requesting approval verify

- Target remains in scope
- Rules of Engagement still valid
- Finding confidence is HIGH or VERIFIED
- Required evidence exists

Approval SHALL NOT be requested for speculative findings.

---

# Preconditions

Before validation begins

Verify

```
Approval Status = APPROVED
```

AND

```
Assessment State = WAITING_APPROVAL
```

---

# Approval Expiration

Approvals SHOULD expire after a configurable duration.

When expired

```
APPROVAL

↓

EXPIRED

↓

Validation Cancelled
```

A new approval request MUST be generated.

---

# Approval Audit Trail

Every approval SHALL record

- Reviewer
- Timestamp
- Decision
- Justification
- Requested Agent
- Requested Action
- Assessment ID

Approval records SHALL be immutable.

---

# Rejected Approval

If approval is rejected

The Master Agent SHALL

- Cancel the validation task
- Preserve the finding
- Mark finding as "Unverified"
- Continue other assessment activities where possible
- Record the rejection

---

# Partial Approval

A reviewer MAY approve only selected validation tasks.

Example

```
Approve

✓ SQL Injection

✗ File Upload

✓ JWT Validation
```

Only approved tasks SHALL execute.

---

# Emergency Stop

A reviewer MAY immediately stop

- Validation
- Exploitation
- Entire Assessment

The Master Agent SHALL cancel all running validation tasks gracefully.

---

# Safety Principles

The Approval Policy SHALL always

- Protect customer systems
- Minimize operational risk
- Require explicit consent
- Preserve auditability
- Prevent accidental exploitation

---

# Quality Checklist

Before dispatching a validation task verify

✅ Approval received

✅ Approval not expired

✅ Task matches approval

✅ Scope validated

✅ Rules of Engagement satisfied

✅ Required evidence exists

✅ Read-only validation confirmed

---

# Guiding Principles

The Master Agent SHALL

- Never assume approval
- Never bypass approval
- Never execute intrusive validation automatically
- Always preserve an audit trail
- Always respect customer intent
- Always fail safely