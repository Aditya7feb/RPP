# Skill Execution Model

**File:** `skills/core/execution-model.md`

**Version:** 1.0.0

---

# Purpose

The Skill Execution Model defines how skills are invoked, controlled, monitored, and terminated within the Robust PenTest Platform (RPP).

It establishes a common execution contract between the Master Agent, execution engine, scheduler, and every skill.

This document defines execution semantics rather than implementation details.

---

# Design Principles

Skill execution SHALL be

- Deterministic
- Observable
- Recoverable
- Interruptible
- Configurable
- Auditable
- Platform Independent

Execution behavior SHALL remain consistent regardless of runtime or programming language.

---

# Relationship

```
Assessment

↓

Execution Plan

↓

Task

↓

Master Agent

↓

Execution Engine

↓

Skill

↓

Agent Response
```

The Execution Engine SHALL invoke skills according to the Execution Plan.

---

# Execution Context

Every skill SHALL execute within an isolated execution context.

The execution context SHALL include

```yaml
assessment:

task:

target:

configuration:

runtime:

technology_inventory:

previous_evidence:

execution_metadata:
```

Skills SHALL NOT depend on global runtime state.

---

# Execution Modes

Supported execution modes include

```
Synchronous

Asynchronous

Streaming

Scheduled
```

Additional modes MAY be introduced in future versions.

---

## Synchronous Execution

The caller waits until execution completes.

Typical examples

- DNS Resolution
- JWT Parsing
- TLS Inspection

Suitable for short-running operations.

---

## Asynchronous Execution

Execution continues independently after invocation.

Typical examples

- Port Scanning
- Directory Enumeration
- Nuclei Scans

The Master Agent SHALL monitor progress through the Execution State.

---

## Streaming Execution

A skill MAY emit incremental results before completion.

Examples

- Endpoint discovery
- Live crawling
- Port scanning
- Log analysis

Streaming SHALL preserve output ordering where required.

---

## Scheduled Execution

Execution MAY be deferred until

- Dependencies are satisfied
- Approval is granted
- Resource limits allow execution
- Time-based constraints are met

---

# Execution Flow

```
Receive Task

↓

Create Execution Context

↓

Validate Inputs

↓

Allocate Resources

↓

Execute Capability

↓

Collect Evidence

↓

Generate Results

↓

Cleanup

↓

Return Agent Response
```

This sequence SHALL align with the Skill Lifecycle.

---

# Resource Management

The execution engine SHALL manage

```yaml
cpu:

memory:

network:

disk:

temporary_storage:
```

Skills SHOULD release allocated resources during cleanup.

---

# Timeouts

Each execution MAY define

```yaml
timeout:

maximum_runtime:

idle_timeout:
```

Timeout policies SHALL be configurable.

A timeout SHALL result in graceful termination whenever possible.

---

# Cancellation

Execution MAY be cancelled by

- Master Agent
- Human Operator
- Policy Engine
- System Shutdown

Cancellation SHOULD trigger

1. Stop execution
2. Preserve collected evidence
3. Execute cleanup
4. Return partial results where possible

---

# Retry Model

Retries SHALL follow the Retry Policy.

Typical retry conditions

- Temporary network failures
- DNS failures
- Rate limiting
- Service unavailability

Retries SHOULD NOT occur for

- Invalid input
- Authorization failures
- Unsupported targets
- Permanent configuration errors

---

# Concurrency

Multiple skills MAY execute concurrently.

Execution SHALL respect

```yaml
maximum_parallel_tasks:

resource_limits:

dependency_graph:

approval_constraints:
```

Skills SHALL remain thread-safe or process-safe where applicable.

---

# Dependency Resolution

Execution SHALL begin only after

- Required dependencies complete successfully
- Required technologies are identified
- Required approvals are granted
- Required inputs become available

The scheduler SHALL enforce dependency ordering.

---

# Context Propagation

Execution context SHALL be propagated between dependent skills.

Examples include

- Technology Inventory
- Evidence References
- Authentication State
- Session Information
- Cookies
- Tokens
- Discovered Endpoints

Skills SHALL consume context rather than rediscover it where appropriate.

---

# Error Propagation

Execution failures SHALL return structured errors.

Errors SHALL include

```yaml
severity:

component:

message:

recoverable:
```

Errors SHALL conform to the Agent Response schema.

---

# Observability

Every execution SHALL emit runtime events.

Examples

- Started
- Paused
- Resumed
- Waiting
- Retrying
- Completed
- Failed
- Cancelled

These events SHOULD update the Execution State.

---

# Progress Reporting

Long-running skills SHOULD report

```yaml
progress:

current_step:

estimated_remaining:

items_processed:
```

Progress reporting enables runtime monitoring.

---

# Evidence Publication

Evidence MAY be published

- Continuously
- At stage completion
- At execution completion

Evidence SHALL conform to the canonical Evidence schema.

---

# Result Generation

Every execution SHALL produce a standardized Agent Response.

Results MAY include

- Findings
- Evidence
- Technologies
- Recommendations
- Metrics
- Errors

Execution SHALL NOT return implementation-specific formats.

---

# Cleanup

Execution SHALL always perform cleanup.

Typical cleanup includes

- Closing sockets
- Terminating browser sessions
- Deleting temporary files
- Releasing credentials
- Flushing logs
- Releasing memory

Cleanup SHALL occur regardless of execution outcome.

---

# Recovery

The execution engine SHOULD support recovery after interruption.

Recoverable state MAY include

- Execution Context
- Progress
- Collected Evidence
- Runtime Metrics
- Checkpoints

Recovery SHOULD avoid repeating completed work.

---

# Security Considerations

Execution SHALL

- Respect Rules of Engagement
- Respect Approval Policies
- Honor Rate Limits
- Prevent Scope Expansion
- Protect Sensitive Data
- Record Audit Events

---

# Validation Rules

A compliant execution model SHALL

- Create an execution context
- Validate inputs
- Enforce dependencies
- Support cancellation
- Support retries
- Preserve evidence
- Produce Agent Responses
- Execute cleanup

---

# Quality Requirements

The execution model SHALL

✓ Be deterministic

✓ Be observable

✓ Support synchronous and asynchronous execution

✓ Preserve execution context

✓ Support recovery

✓ Enforce resource constraints

✓ Generate standardized outputs

✓ Remain platform independent

---

# Future Extensions

Future versions MAY include

- Distributed execution
- Remote skill workers
- Execution sandboxing
- GPU scheduling
- Cost-aware scheduling
- Priority-based execution
- Multi-region execution
- Streaming checkpoints

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Execution Model provides a predictable, observable, and recoverable mechanism for executing skills within the Robust PenTest Platform.

It enables the Master Agent to orchestrate heterogeneous skills consistently while preserving execution integrity, auditability, and interoperability across the platform.