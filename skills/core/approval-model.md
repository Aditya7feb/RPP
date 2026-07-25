# Skill Approval Model

**File:** `skills/core/approval-model.md`

**Version:** 1.0.0

---

# Purpose

The Skill Approval Model defines when skill execution requires authorization, how approvals are represented, and how approval decisions influence execution within the Robust PenTest Platform (RPP).

The approval model ensures autonomous execution remains aligned with organizational policies, rules of engagement, and assessment objectives.

Approval requirements SHALL be declarative, auditable, and independent of implementation.

---

# Design Principles

Approval decisions SHALL be

- Explicit
- Policy Driven
- Auditable
- Least Privilege
- Scope Aware
- Deterministic
- Independent of Runtime

No skill SHALL assume approval has been granted.

---

# Relationship

```
Assessment

↓

Execution Plan

↓

Task

↓

Approval Evaluation

↓

Approved?

├── Yes → Execute Skill
└── No  → Waiting for Approval
```

Approval SHALL be evaluated before execution begins.

---

# Approval Objectives

The approval model exists to

- Prevent unintended actions
- Protect production systems
- Enforce Rules of Engagement
- Enable human oversight
- Reduce operational risk
- Maintain accountability

---

# Approval Levels

Supported approval levels

```
None

↓

Automatic

↓

Operator

↓

Security Lead

↓

Assessment Owner

↓

Organization Approval
```

Organizations MAY define additional approval levels.

---

# Approval Modes

Supported modes

```
Pre-Execution

Runtime

Post-Execution
```

---

## Pre-Execution

Approval is required before execution begins.

Example

```
Authenticated Testing

↓

Approval

↓

Execute
```

---

## Runtime

Execution pauses until approval is granted.

Example

```
Discovery

↓

Potential Exploitation

↓

Approval

↓

Continue
```

---

## Post-Execution

Execution completes, but results require review before publication.

Example

```
Evidence Collected

↓

Review

↓

Report Published
```

---

# Approval Triggers

Approval MAY be required for

- Exploitation
- Credential Usage
- State-Changing Operations
- Destructive Testing
- Privilege Escalation
- Denial-of-Service Testing
- Data Extraction
- Cloud Resource Modification
- External Service Interaction
- Out-of-Scope Expansion

Organizations MAY define additional triggers.

---

# Automatic Approval

Execution MAY proceed automatically when

- Capability is classified as safe
- Policy allows autonomous execution
- Scope is validated
- Required dependencies are satisfied

Automatic approval SHALL be recorded.

---

# Approval Request

Every approval request SHOULD include

```yaml
approval_id:

assessment:

task:

skill:

requested_action:

reason:

risk_level:

requested_by:

timestamp:
```

---

# Approval Decision

Every approval decision SHALL record

```yaml
status:

approved_by:

decision:

reason:

timestamp:

expires_at:
```

Supported decisions

```
Approved

Rejected

Expired

Cancelled
```

---

# Approval States

Every approval SHALL exist in one of the following states

```
Pending

Approved

Rejected

Expired

Cancelled
```

Approval state SHALL be tracked in the Execution State.

---

# Approval Scope

Approval MAY apply to

- Assessment
- Workflow
- Task
- Capability
- Skill
- Target
- Resource

Example

```
Approve

↓

Authenticated Scanning

↓

Target A Only
```

Approvals SHALL NOT automatically extend beyond their defined scope.

---

# Approval Expiration

Approvals MAY expire.

Expired approvals SHALL NOT authorize future execution.

Expired approvals MAY require re-submission.

---

# Conditional Approval

Approvals MAY define execution constraints.

Examples

- Maximum request rate
- Allowed targets
- Allowed capabilities
- Time window
- Maximum duration
- Maximum concurrency

Execution SHALL comply with all defined conditions.

---

# Approval Revocation

Previously granted approval MAY be revoked.

Upon revocation

- Running tasks SHOULD stop safely
- Evidence SHALL be preserved
- Execution State SHALL be updated
- Audit events SHALL be recorded

---

# Policy Integration

Approval evaluation SHALL consider

- Rules of Engagement
- Organizational Policy
- Target Classification
- Assessment Scope
- Capability Classification
- Risk Level

Policies SHALL take precedence over skill defaults.

---

# Audit Requirements

Every approval event SHALL be auditable.

Audit information SHOULD include

```yaml
approval_id:

assessment:

task:

actor:

decision:

timestamp:

reason:
```

---

# Failure Handling

If approval is

Rejected

↓

Execution SHALL NOT begin.

If approval expires during execution

↓

Execution SHALL follow organizational policy.

Possible actions

- Continue
- Pause
- Stop
- Escalate

---

# Reporting

Approval history SHOULD be available for

- Assessments
- Tasks
- Skills
- Findings

Reports MAY include approval references where appropriate.

---

# Validation Rules

A compliant approval model SHALL

- Define approval requirements
- Support approval states
- Support approval scopes
- Support expiration
- Support revocation
- Record audit information

---

# Quality Requirements

The approval model SHALL

✓ Enforce policy before execution

✓ Support human oversight

✓ Preserve auditability

✓ Support scoped approvals

✓ Prevent unauthorized execution

✓ Support expiration and revocation

✓ Integrate with execution planning

✓ Remain implementation independent

---

# Future Extensions

Future versions MAY include

- Multi-party approval
- Risk-adaptive approval
- Emergency approval workflows
- Just-in-time approval
- Delegated approval
- AI-assisted approval recommendations

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Approval Model provides a standardized mechanism for authorizing potentially impactful operations before execution.

It enables the Robust PenTest Platform to balance autonomous operation with organizational governance, ensuring that high-risk capabilities are executed only with appropriate authorization while maintaining traceability and accountability.