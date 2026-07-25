# Task Schema

**File:** `schemas/task.md`

**Version:** 1.0.0

---

# Purpose

The Task Schema defines the canonical representation of a unit of work within the Robust PenTest Platform (RPP).

Every piece of work performed during an assessment SHALL be represented as a Task.

Tasks provide a consistent mechanism for planning, scheduling, execution, monitoring, and auditing.

No agent SHALL execute work outside a Task.

---

# Design Principles

A Task SHALL be

- Atomic
- Traceable
- Deterministic
- Idempotent
- Versioned
- Observable
- Auditable

---

# Task Lifecycle

```
Created

↓

Queued

↓

Ready

↓

Running

↓

Completed

↓

Archived
```

Alternative paths

```
Running

↓

Failed
```

```
Running

↓

Cancelled
```

```
Queued

↓

Skipped
```

---

# Identity

Every task SHALL contain

```yaml
task_id:

assessment_id:

schema_version:
```

Task IDs SHALL be globally unique within an assessment.

---

# Ownership

Every task SHALL have

```yaml
owner:

assigned_agent:

created_by:
```

Example

```yaml
owner: Master Agent

assigned_agent: DNS Agent

created_by: Planning Agent
```

---

# Task Classification

Every task SHALL define

```yaml
category:

capability:

phase:
```

Example

```yaml
category: Recon

capability: DNS Enumeration

phase: Reconnaissance
```

---

# Target

Each task SHALL explicitly define its target.

```yaml
target:

type:

scope:
```

Examples

```
example.com
```

```
192.168.1.0/24
```

```
https://example.com/login
```

---

# Priority

Allowed values

```
Critical

High

Medium

Low
```

Priority determines scheduling preference.

Priority SHALL NOT modify severity.

---

# Status

Allowed values

```
CREATED

QUEUED

READY

RUNNING

WAITING

COMPLETED

FAILED

SKIPPED

BLOCKED

CANCELLED
```

Status transitions SHALL follow the lifecycle rules.

---

# Dependencies

Tasks MAY depend upon other tasks.

```yaml
depends_on:

required_outputs:
```

Example

```
Technology Detection

↓

Content Discovery

↓

GraphQL Discovery
```

The Master Agent SHALL enforce dependency ordering.

---

# Inputs

Every task SHALL specify

```yaml
inputs:

assessment:

scope:

configuration:

previous_results:
```

Tasks SHALL NOT infer missing inputs.

---

# Outputs

Every completed task SHALL produce

```yaml
outputs:

findings:

evidence:

metadata:

execution_summary:
```

Tasks MAY return empty findings if no issues are discovered.

---

# Execution Metadata

Each task SHALL record

```yaml
execution:

started_at:

completed_at:

runtime:

retry_count:
```

---

# Progress

Long-running tasks SHOULD report

```yaml
progress:

percentage:

current_step:

estimated_remaining:
```

---

# Failure Information

Failed tasks SHALL include

```yaml
failure:

reason:

recoverable:

retry_recommended:

error_code:
```

Failure SHALL NEVER discard collected evidence.

---

# Retry Policy

Tasks MAY be retried when

- Temporary network failure
- Agent unavailable
- Timeout
- Recoverable tool failure

Tasks SHALL NOT retry when

- Scope invalid
- Approval denied
- Unsupported capability
- Permanent configuration error

---

# Approval Requirements

Tasks SHALL declare

```yaml
approval_required:

approval_status:
```

Validation tasks SHOULD require approval.

Reconnaissance tasks normally SHALL NOT.

---

# Evidence

Tasks SHALL reference collected evidence.

```yaml
evidence:

- evidence_id
- evidence_id
- evidence_id
```

Evidence SHALL NOT be embedded directly inside the task.

---

# Findings

Tasks MAY produce

```yaml
findings:

- finding_id
- finding_id
```

Tasks without findings remain valid.

---

# Logging

Every task SHALL produce

- Start timestamp
- End timestamp
- Assigned agent
- Final status
- Runtime
- Execution summary

---

# Relationships

```
Assessment

↓

Task

↓

Finding

↓

Evidence
```

Tasks SHALL NOT exist without an Assessment.

---

# Validation Rules

A valid task SHALL contain

- Task ID
- Assessment ID
- Assigned Agent
- Capability
- Target
- Status
- Schema Version

---

# Future Extensions

Future versions MAY include

- Resource limits
- Cost estimation
- Scheduling windows
- Required credentials
- Tool preferences
- Estimated duration

Existing implementations SHOULD remain compatible.

---

# Success Criteria

A compliant Task object represents a complete, traceable, executable unit of work.

Every action performed by the platform SHALL be traceable to one or more Tasks.

No work SHALL occur outside the Task model.