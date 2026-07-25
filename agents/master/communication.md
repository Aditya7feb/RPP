# Master Agent Communication Contract

**File:** `agents/master/communication.md`

**Version:** 1.0.0

---

# Purpose

The Communication Contract defines how the Master Agent exchanges information with specialist agents throughout an assessment.

The objective is to ensure every interaction is predictable, traceable, versioned, and independent of implementation technology.

This contract applies equally whether agents communicate via:

- MCP
- REST APIs
- Message Queues
- Local Process Calls
- Agent Frameworks
- Future Transport Mechanisms

The transport mechanism SHALL NOT affect the communication model.

---

# Design Principles

Communication SHALL be

- Structured
- Deterministic
- Versioned
- Idempotent
- Traceable
- Observable
- Extensible

---

# Communication Lifecycle

```
Assessment Created

↓

Task Generated

↓

Task Assigned

↓

Agent Executes

↓

Progress Updates

↓

Task Completed

↓

Evidence Returned

↓

Assessment Updated
```

---

# Communication Roles

## Master Agent

Responsible for

- Creating tasks
- Scheduling work
- Tracking execution
- Receiving results
- Updating assessment state

The Master Agent SHALL NOT execute specialist logic.

---

## Specialist Agent

Responsible for

- Accepting assigned tasks
- Executing domain-specific work
- Collecting evidence
- Reporting findings
- Reporting status
- Returning structured responses

Specialist agents SHALL NOT modify assessment state directly.

---

# Message Types

The platform defines the following logical message types.

```
ASSESSMENT_CREATED

TASK_CREATED

TASK_ASSIGNED

TASK_ACCEPTED

TASK_STARTED

TASK_PROGRESS

TASK_COMPLETED

TASK_FAILED

TASK_CANCELLED

EVIDENCE_CREATED

FINDING_CREATED

APPROVAL_REQUIRED

APPROVAL_RECEIVED

ASSESSMENT_UPDATED

ASSESSMENT_COMPLETED
```

---

# Task Structure

Every task SHALL contain

```yaml
task_id:

assessment_id:

agent:

capability:

priority:

scope:

dependencies:

status:

created_at:
```

---

# Status Updates

Agents SHALL report state transitions.

Allowed states

```
PENDING

READY

RUNNING

WAITING

COMPLETED

FAILED

SKIPPED

BLOCKED

CANCELLED
```

State transitions SHALL be valid and chronological.

---

# Progress Reporting

Long-running tasks SHOULD periodically report progress.

Progress MAY include

```yaml
percentage:

current_step:

estimated_remaining_time:

discovered_items:
```

Progress updates SHALL NOT contain partial findings unless explicitly supported.

---

# Findings

Every finding SHALL include

```yaml
finding_id:

title:

description:

severity:

confidence:

status:

affected_target:

evidence:
```

Findings SHALL NOT omit evidence references.

---

# Evidence References

Agents SHALL exchange evidence identifiers rather than duplicating artifacts.

Example

```yaml
evidence:

- EVD-000123
- EVD-000124
```

Evidence SHALL remain immutable after creation.

---

# Error Reporting

Failures SHALL be reported in a structured format.

```yaml
error_code:

error_type:

message:

recoverable:

retry_recommended:
```

Human-readable messages SHOULD accompany machine-readable codes.

---

# Retry Behaviour

If a task fails

The specialist agent SHALL report the failure.

The Master Agent determines whether a retry is appropriate.

Specialist agents SHALL NOT retry indefinitely without coordination.

---

# Cancellation

Cancellation requests SHALL be acknowledged.

When cancellation occurs

The agent SHALL

- Stop execution safely
- Preserve collected evidence
- Report final status

---

# Timeouts

Agents SHOULD report

- Start time
- End time
- Runtime

If execution exceeds expected limits

A timeout status SHALL be returned.

---

# Version Compatibility

Every communication SHALL include

```yaml
protocol_version:

agent_version:
```

The Master Agent SHALL reject incompatible protocol versions.

---

# Idempotency

Repeated delivery of the same message SHALL NOT create duplicate

- Tasks
- Findings
- Evidence
- Status Updates

Every message SHALL contain a unique identifier.

---

# Observability

All communications SHOULD be logged.

Each log entry SHOULD include

- Timestamp
- Sender
- Receiver
- Message Type
- Correlation ID
- Task ID
- Assessment ID

Logs SHALL NOT contain sensitive secrets unless explicitly required.

---

# Correlation

Every message SHALL be traceable.

Minimum identifiers

```yaml
assessment_id:

task_id:

correlation_id:
```

These identifiers SHALL remain constant throughout the task lifecycle.

---

# Security Requirements

Communication SHALL

- Validate message integrity
- Authenticate participating agents
- Authorize requested actions
- Protect sensitive metadata
- Prevent replay where applicable

Security mechanisms are implementation-specific and outside the scope of this document.

---

# Extensibility

Agents MAY introduce additional fields.

Unknown optional fields SHALL be ignored rather than rejected.

Required fields SHALL remain stable across protocol versions.

---

# Quality Checklist

Before accepting a message verify

✅ Protocol version supported

✅ Required fields present

✅ Assessment ID valid

✅ Task ID valid

✅ Message type recognized

✅ Status transition valid

✅ Evidence references valid

✅ Correlation ID present

---

# Guiding Principles

The Master Agent SHALL

- Treat communication as a contract
- Separate transport from message structure
- Preserve traceability
- Ensure deterministic behaviour
- Never lose message attribution
- Support future protocol evolution without breaking compatibility

---

# Success Criteria

The communication model is successful when

- Every task is traceable from creation to completion
- Every finding can be linked to its originating task
- Every evidence item can be traced to its source
- Agents remain loosely coupled
- New agents can be introduced without changing existing communication semantics