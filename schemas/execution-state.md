# Execution State Schema

**File:** `schemas/execution-state.md`

**Version:** 1.0.0

---

# Purpose

The Execution State Schema defines the canonical representation of the runtime state of an assessment within the Robust PenTest Platform (RPP).

While the Execution Plan defines the intended workflow, the Execution State captures the current progress, active work, completed work, failures, runtime metrics, and orchestration status.

The Execution State SHALL represent the single source of truth for assessment execution.

---

# Design Principles

An Execution State SHALL be

- Real-time
- Versioned
- Auditable
- Recoverable
- Observable
- Traceable
- Implementation-independent

Unlike most schemas, the Execution State is expected to change throughout the assessment lifecycle.

---

# Relationship

```
Assessment
    │
    ├── Execution Plan
    │
    └── Execution State
             │
             ├── Active Tasks
             ├── Queue
             ├── Running Agents
             ├── Runtime Metrics
             └── Progress
```

---

# Identity

Every Execution State SHALL contain

```yaml
execution_state_id:

assessment_id:

execution_plan_id:

schema_version:
```

---

# Metadata

Every Execution State SHALL record

```yaml
created_at:

last_updated:

updated_by:

revision:
```

Each update SHALL increment the revision number.

---

# Assessment Status

Allowed values

```
Created

Planning

Ready

Running

Paused

Waiting For Approval

Completed

Failed

Cancelled

Archived
```

Only valid lifecycle transitions SHALL be permitted.

---

# Stage Status

Each execution stage SHALL include

```yaml
stage:

status:

started_at:

completed_at:
```

Supported status values

```
Pending

Running

Completed

Failed

Skipped

Blocked
```

---

# Task Summary

Execution State SHALL summarize task progress.

```yaml
tasks:

total:

queued:

running:

completed:

failed:

blocked:

cancelled:
```

---

# Active Tasks

The currently executing tasks SHALL be recorded.

```yaml
active_tasks:

- task_id

- task_id
```

Tasks SHALL reference Task objects rather than embedding them.

---

# Task Queue

The scheduler SHALL maintain

```yaml
queued_tasks:

- task_id

- task_id
```

Queue ordering MAY change during adaptive replanning.

---

# Completed Tasks

Execution State SHALL maintain

```yaml
completed_tasks:

- task_id
```

---

# Failed Tasks

Failures SHALL include

```yaml
failed_tasks:

- task_id:

  reason:

  timestamp:
```

Task failure history SHALL be preserved.

---

# Running Agents

Execution State SHALL record

```yaml
agents:

agent_name:

status:

current_task:

started_at:
```

Supported statuses

```
Idle

Running

Waiting

Paused

Completed

Failed
```

---

# Approval State

Execution SHALL track pending approvals.

```yaml
approvals:

pending:

approved:

rejected:
```

Pending approvals SHALL block dependent tasks.

---

# Runtime Metrics

Execution State SHOULD include

```yaml
runtime:

elapsed_time:

estimated_remaining:

cpu_usage:

memory_usage:

network_requests:
```

Implementations MAY expose additional metrics.

---

# Progress

Overall assessment progress SHALL include

```yaml
progress:

percentage:

current_stage:

current_task:

remaining_tasks:
```

Progress SHOULD be calculated automatically.

---

# Findings Summary

Execution SHALL summarize discoveries.

```yaml
findings:

critical:

high:

medium:

low:

informational:
```

Only verified Findings SHOULD contribute to summary statistics unless configured otherwise.

---

# Evidence Summary

Execution State SHALL include

```yaml
evidence:

total:

validated:

pending_processing:
```

---

# Technology Summary

Execution State MAY maintain

```yaml
technologies:

detected:

verified:

pending_validation:
```

---

# Dynamic Events

Execution SHALL record significant runtime events.

Examples

- New Host Discovered
- Technology Identified
- Approval Granted
- Task Failed
- Scope Updated
- Agent Restarted

```yaml
events:

- timestamp:

  type:

  description:
```

---

# Checkpoints

Execution State SHOULD support recovery.

```yaml
checkpoint:

checkpoint_id:

created_at:

recoverable:
```

The Master Agent MAY resume execution from the latest valid checkpoint.

---

# Error Handling

Runtime errors SHALL include

```yaml
errors:

severity:

component:

message:

timestamp:
```

Supported severities

```
Info

Warning

Error

Critical
```

---

# Cancellation

Execution State SHALL record

```yaml
cancelled_by:

cancelled_at:

reason:
```

---

# Completion

Upon successful completion

```yaml
completed_at:

duration:

report_generated:
```

---

# Validation Rules

A valid Execution State SHALL contain

- Execution State ID
- Assessment ID
- Execution Plan ID
- Assessment Status
- Stage Status
- Task Summary
- Progress
- Schema Version

---

# Quality Requirements

Execution State SHALL

✓ Represent current runtime state

✓ Preserve execution history

✓ Support recovery

✓ Track approvals

✓ Track agent activity

✓ Track progress

✓ Support dynamic replanning

---

# Future Extensions

Future versions MAY include

- Distributed execution status
- Cluster node health
- Cost tracking
- Token usage
- Agent heartbeat monitoring
- Predictive completion estimates
- SLA monitoring
- Real-time dashboards

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Execution State provides a complete, real-time, and recoverable view of an assessment in progress.

It SHALL be the authoritative runtime representation used by the Master Agent for orchestration, monitoring, recovery, and reporting.