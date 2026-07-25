# Approval Schema

**File:** `schemas/approval.md`

**Version:** 1.0.0

---

# Purpose

The Approval Schema defines the canonical representation of a human approval request within the Robust PenTest Platform (RPP).

Approval objects are used to authorize actions that may be intrusive, state-changing, or otherwise require explicit human consent.

Approval SHALL be independent of the underlying implementation.

---

# Design Principles

An Approval SHALL be

- Human initiated
- Traceable
- Auditable
- Immutable
- Versioned
- Time bounded
- Evidence-backed

Approval SHALL NEVER be assumed.

---

# Relationship

```
Assessment
    │
    ├── Finding
    │
    ├── Validation Task
    │
    └── Approval
```

An Approval MAY authorize one or more validation tasks.

---

# Identity

Every Approval SHALL contain

```yaml
approval_id:

assessment_id:

schema_version:
```

Approval IDs SHALL be globally unique within an assessment.

---

# Approval Request

Every request SHALL define

```yaml
title:

description:

reason:

requested_by:

requested_at:
```

The request SHALL clearly explain

- Why approval is required
- What action is proposed
- Expected outcome
- Potential impact

---

# Approval Scope

Every Approval SHALL specify

```yaml
scope:

targets:

tasks:

findings:

validation_agents:
```

Approval SHALL apply only to the defined scope.

---

# Approval Type

Supported values

```
Validation

Exploitation

Credential Usage

Authenticated Testing

Custom
```

Future approval types MAY be added.

---

# Status

Allowed values

```
Pending

Approved

Rejected

Expired

Cancelled
```

Only valid state transitions SHALL be permitted.

---

# Reviewer Information

Every decision SHALL record

```yaml
reviewed_by:

reviewed_at:

decision:
```

---

# Decision

Allowed values

```
Approve

Reject

Request Changes

Cancel
```

---

# Decision Notes

Reviewers MAY provide

```yaml
comments:

limitations:

conditions:
```

Example

```
Validate SQL Injection

Only against staging environment

Maximum duration: 30 minutes
```

---

# Expiration

Approval SHALL define

```yaml
expires_at:

expired:
```

Expired approvals SHALL NOT authorize execution.

---

# Related Objects

Approval MAY reference

```yaml
tasks:

findings:

evidence:

execution_plan:
```

---

# Risk Assessment

Approval SHOULD include

```yaml
estimated_impact:

risk_level:

expected_requests:

rollback_required:
```

---

# Preconditions

Before execution verify

```
Status = Approved
```

AND

```
Current Time < Expiration
```

AND

```
Task within Approved Scope
```

---

# Audit Trail

Every Approval SHALL record

```yaml
created_at:

updated_at:

review_history:
```

Review history SHOULD preserve all decisions.

---

# Validation Rules

A valid Approval SHALL contain

- Approval ID
- Assessment ID
- Status
- Reviewer (if completed)
- Decision
- Scope
- Expiration

---

# Quality Requirements

Approval SHALL

✓ Define scope

✓ Record reviewer

✓ Record timestamps

✓ Preserve history

✓ Be immutable after decision

✓ Be auditable

---

# Future Extensions

Future versions MAY include

- Multi-stage approval workflows
- Multiple reviewers
- Digital signatures
- Risk scoring integrations
- Policy engine integration
- Organization-specific approval rules

Backward compatibility SHOULD be preserved.

---

# Success Criteria

A compliant Approval object provides an auditable, traceable, and enforceable authorization mechanism for high-risk assessment activities.

Every validation or intrusive action requiring authorization SHALL reference a valid Approval object.