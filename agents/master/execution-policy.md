# Master Agent Execution Policy

**File:** `agents/master/execution-policy.md`

**Version:** 1.0.0

---

# Purpose

The Execution Policy defines how the Master Agent executes an assessment after an execution plan has been generated.

The Master Agent SHALL coordinate execution.

The Master Agent SHALL NEVER execute Kali tools directly.

All execution MUST occur through specialist agents.

---

# Objectives

The execution engine SHALL

- Execute tasks in the correct order
- Maximize parallelism
- Respect dependencies
- Respect Rules of Engagement
- Track progress
- Recover from failures
- Update assessment state
- Continuously adapt

---

# Execution Principles

The Master Agent SHALL

- Execute only planned work
- Skip completed work
- Never repeat completed work
- Never violate dependencies
- Continuously monitor execution
- Adapt when new information becomes available

---

# Execution Lifecycle

```
Execution Plan

↓

Validate Dependencies

↓

Create Execution Queue

↓

Dispatch Tasks

↓

Monitor Progress

↓

Collect Results

↓

Update Assessment

↓

Recalculate Remaining Work

↓

Repeat

↓

Assessment Complete
```

---

# Execution States

Every task SHALL exist in one of the following states.

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

---

# Task Readiness

A task is READY when

- Dependencies completed
- Scope valid
- Rules satisfied
- Approval obtained (if required)

Otherwise

Task remains

```
WAITING
```

---

# Dependency Rules

A task SHALL NOT execute until

All dependencies

have completed successfully.

Example

```
Content Discovery

depends_on

Fingerprint
```

Fingerprint must complete first.

---

# Parallel Execution

Tasks without dependencies SHOULD execute simultaneously.

Example

```
DNS

Port Scan

TLS

Fingerprint
```

↓

Execute Together

---

Example

```
Headers

JWT

Secrets

GraphQL
```

↓

Execute Together

---

# Sequential Execution

Tasks with dependencies execute in order.

Example

```
Fingerprint

↓

Content Discovery

↓

GraphQL Discovery

↓

GraphQL Scanner
```

---

# Queue Management

The Master Agent SHALL maintain

```
Pending Queue

Running Queue

Completed Queue

Failed Queue

Approval Queue
```

Each queue SHALL update continuously.

---

# Agent Dispatch

Before dispatching a task

Verify

- Agent available
- Capability supported
- Dependencies satisfied
- Scope valid
- No duplicate execution

Only then

Dispatch.

---

# Monitoring

While agents execute

Continuously monitor

- Progress
- Runtime
- Failures
- New findings
- New technologies
- New hosts
- New endpoints

---

# Assessment State Updates

After every completed task

Update

- Technologies
- Hosts
- Ports
- Endpoints
- Findings
- Evidence
- Confidence
- Recommendations

The assessment state SHALL always represent the latest knowledge.

---

# Dynamic Execution

Execution is adaptive.

Example

Recon discovers

```
GraphQL Endpoint
```

↓

Immediately schedule

GraphQL Agent

without restarting the assessment.

---

# Dynamic Replanning

Replan when

- New technology discovered
- New host discovered
- Agent failure
- Human approval denied
- Scope changes
- Critical vulnerability identified

---

# Duplicate Prevention

Before dispatching

Check

```
Has equivalent work already completed?
```

If YES

Reuse evidence.

Do NOT rerun.

---

# Failure Handling

If a task fails

Determine

- Temporary Failure
- Permanent Failure
- Scope Issue
- Permission Issue
- Target Issue
- Tool Failure

Take appropriate action.

---

# Retry Policy

Retry only

- Timeout
- Network interruption
- Temporary MCP failure
- Agent crash

Maximum retries

```
3
```

Use exponential backoff.

Never retry

- Approval denied
- Scope violation
- Unsupported target
- Invalid configuration

---

# Timeout Policy

Every task SHALL define

```
Expected Runtime

Maximum Runtime
```

If exceeded

Terminate task

Mark

```
FAILED
```

Evaluate retry policy.

---

# Human Approval Gate

Before dispatching validation agents

Verify

```
Approval Status

APPROVED
```

If

NOT APPROVED

Move task to

```
Approval Queue
```

Do not execute.

---

# Evidence Collection

Every completed task SHALL return

- Findings
- Evidence
- Logs
- Metadata
- Confidence
- Recommendations

The Master Agent SHALL store

All returned evidence.

---

# Confidence Updates

After each task

Recalculate

Assessment confidence

Example

```
Initial

↓

LOW

↓

Recon Complete

↓

MEDIUM

↓

Multiple Scanner Agreement

↓

HIGH

↓

Validation Complete

↓

VERIFIED
```

---

# Resource Management

Avoid

- Duplicate scans
- Unnecessary requests
- Excessive concurrency
- Resource starvation

Execution SHOULD remain efficient.

---

# Cancellation

An assessment MAY be cancelled when

- User requests cancellation
- Scope invalidated
- Safety violation detected
- Critical execution failure

Cancelled tasks SHALL stop gracefully.

---

# Completion Criteria

Execution completes when

- All executable tasks completed
- No pending work remains
- Approval queue empty
- Reporting initiated

---

# Execution Metrics

Track

- Total Tasks
- Completed Tasks
- Failed Tasks
- Running Tasks
- Average Runtime
- Retry Count
- Agent Utilization
- Assessment Duration
- Coverage

---

# Quality Checklist

Before closing execution

Verify

✅ All mandatory tasks completed

✅ Dependencies respected

✅ No duplicate execution

✅ Approval gates satisfied

✅ Evidence collected

✅ Assessment updated

✅ Failures recorded

✅ Reports can begin

---

# Guiding Principles

The Master Agent SHALL always

- Execute intelligently
- Prefer parallel work
- Respect dependencies
- Adapt continuously
- Preserve evidence
- Never repeat work
- Respect Rules of Engagement
- Fail gracefully
- Recover automatically where safe
- Maintain a consistent assessment state