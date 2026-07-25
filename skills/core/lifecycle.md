# Skill Lifecycle

**File:** `skills/core/lifecycle.md`

**Version:** 1.0.0

---

# Purpose

The Skill Lifecycle defines the standard execution lifecycle for every skill within the Robust PenTest Platform (RPP).

Regardless of implementation language, runtime, or execution environment, every skill SHALL follow the same logical lifecycle.

A consistent lifecycle enables predictable orchestration, observability, retries, auditing, error handling, and recovery.

---

# Design Principles

Every skill lifecycle SHALL be

- Deterministic
- Observable
- Auditable
- Recoverable
- Extensible
- Stateless
- Versioned

A skill SHALL progress through defined lifecycle states.

State transitions SHALL be explicit.

---

# Lifecycle Overview

```
Registered

↓

Selected

↓

Initialized

↓

Validated

↓

Prepared

↓

Executing

↓

Collecting Evidence

↓

Generating Results

↓

Completed

↓

Cleaned Up
```

Alternative paths

```
Executing

↓

Failed

↓

Cleanup

↓

Terminated
```

or

```
Validated

↓

Waiting For Approval

↓

Prepared
```

---

# Lifecycle States

## Registered

The skill is known to the platform.

At this stage

- Metadata is available
- Capabilities are discoverable
- Version is known
- Dependencies are declared

No execution occurs.

---

## Selected

The Master Agent selects the skill based on

- Required capability
- Technology inventory
- Assessment scope
- Planning rules
- Dependencies

Selection SHALL NOT execute the skill.

---

## Initialized

The runtime creates the execution context.

Initialization SHOULD include

- Runtime configuration
- Context loading
- Task association
- Assessment association
- Logging initialization

No network operations SHOULD occur.

---

## Validated

Inputs SHALL be validated before execution.

Validation SHOULD verify

- Required inputs
- Configuration
- Scope
- Permissions
- Authentication
- Dependencies

Validation failure SHALL prevent execution.

---

## Waiting For Approval

Some skills require explicit approval.

Examples

- Exploitation
- Authenticated testing
- State-changing operations

Execution SHALL pause until approval is granted.

---

## Prepared

Preparation MAY include

- Authentication
- Session creation
- HTTP client initialization
- Browser startup
- Temporary resource allocation
- Cache loading

Preparation SHALL NOT produce Findings.

---

## Executing

The skill performs its primary operation.

Examples

- Send HTTP request
- Resolve DNS
- Inspect TLS
- Execute Nmap
- Parse HTML
- Validate SQL Injection

Execution SHOULD remain focused on the declared capabilities.

---

## Collecting Evidence

Evidence SHALL be collected throughout execution.

Examples

- HTTP requests
- HTTP responses
- Screenshots
- TLS certificates
- Tool output
- Logs
- Extracted metadata

Evidence SHALL conform to the canonical Evidence schema.

---

## Generating Results

The skill converts observations into structured outputs.

Outputs MAY include

- Evidence references
- Technology references
- Finding references
- Metrics
- Recommendations
- Warnings

The skill SHALL return an Agent Response compatible object.

---

## Completed

Execution finished successfully.

The skill SHALL

- Finalize metrics
- Record execution duration
- Release temporary resources
- Return results

---

## Failed

Execution encountered an unrecoverable error.

Failures SHALL record

- Error type
- Component
- Timestamp
- Recoverability
- Diagnostic information

Partial evidence SHOULD be preserved when possible.

---

## Cleanup

Cleanup SHALL execute regardless of outcome.

Examples

- Close browser
- Close sockets
- Delete temporary files
- Release sessions
- Flush logs
- Persist metrics

Cleanup SHALL be idempotent.

---

## Terminated

The execution context has ended.

No further work SHALL occur.

---

# Lifecycle Transitions

Allowed transitions

```
Registered

↓

Selected

↓

Initialized

↓

Validated

↓

Prepared

↓

Executing

↓

Collecting Evidence

↓

Generating Results

↓

Completed

↓

Cleanup

↓

Terminated
```

Failure path

```
Executing

↓

Failed

↓

Cleanup

↓

Terminated
```

Approval path

```
Validated

↓

Waiting For Approval

↓

Prepared
```

Transitions outside the defined lifecycle SHOULD NOT occur.

---

# State Responsibilities

| State | Primary Responsibility |
|---------|------------------------|
| Registered | Capability discovery |
| Selected | Planning |
| Initialized | Runtime creation |
| Validated | Input verification |
| Waiting For Approval | Human authorization |
| Prepared | Runtime preparation |
| Executing | Capability execution |
| Collecting Evidence | Preserve observations |
| Generating Results | Produce structured outputs |
| Completed | Finalize execution |
| Failed | Record failure |
| Cleanup | Release resources |
| Terminated | End execution |

---

# Observability

Every lifecycle transition SHOULD generate an event.

Example

```yaml
event:

timestamp:

state:

task_id:

skill:

duration:
```

These events SHOULD feed execution monitoring and audit logs.

---

# Retry Behavior

Retries SHALL only occur after

- Validation errors are corrected
- Transient failures are resolved
- Approval is granted
- Retry policy permits execution

A retry SHALL begin from the appropriate lifecycle state rather than always restarting from the beginning.

---

# Recovery

If execution is interrupted

The Master Agent SHOULD resume from the latest recoverable state.

Recoverable states MAY include

- Prepared
- Executing
- Collecting Evidence

Recovery SHALL preserve previously collected evidence.

---

# Metrics

Each lifecycle stage SHOULD record

```yaml
started_at:

completed_at:

duration:

status:
```

Metrics support performance analysis and troubleshooting.

---

# Quality Requirements

Every skill lifecycle SHALL

✓ Validate inputs before execution

✓ Preserve evidence

✓ Generate structured outputs

✓ Support approvals

✓ Support retries

✓ Support cleanup

✓ Support recovery

✓ Remain observable

---

# Validation Rules

A compliant skill SHALL

- Follow the defined lifecycle
- Produce lifecycle events
- Execute cleanup regardless of outcome
- Preserve evidence across failures
- Return a standardized Agent Response

---

# Future Extensions

Future versions MAY include

- Distributed execution checkpoints
- Long-running asynchronous skills
- Streaming results
- Incremental evidence publication
- Parallel lifecycle stages
- Lifecycle policy enforcement

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Skill Lifecycle provides a predictable and auditable execution model for every skill within the Robust PenTest Platform.

Regardless of the capability being performed, every skill SHALL progress through the defined lifecycle, enabling consistent orchestration, monitoring, recovery, and reporting across the platform.