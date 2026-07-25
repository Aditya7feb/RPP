# Execution Plan Schema

**File:** `schemas/execution-plan.md`

**Version:** 1.0.0

---

# Purpose

The Execution Plan Schema defines the canonical representation of an assessment execution strategy within the Robust PenTest Platform (RPP).

An Execution Plan describes **what work will be performed**, **in what order**, **under which conditions**, and **by which agents**.

It is produced during the planning phase and remains the authoritative blueprint for assessment execution.

---

# Design Principles

An Execution Plan SHALL be

- Deterministic
- Adaptive
- Versioned
- Traceable
- Auditable
- Dependency-aware
- Implementation-independent

---

# Relationship

```
Assessment
    │
    ├── Execution Plan
    │       │
    │       ├── Stages
    │       ├── Tasks
    │       ├── Dependencies
    │       ├── Approval Gates
    │       └── Execution Policies
```

---

# Identity

Every Execution Plan SHALL contain

```yaml
execution_plan_id:

assessment_id:

schema_version:
```

---

# Metadata

Every Execution Plan SHALL include

```yaml
name:

description:

created_by:

created_at:

version:
```

---

# Assessment Reference

The plan SHALL reference

```yaml
assessment:

scope:

rules_of_engagement:
```

---

# Execution Stages

Execution SHALL be divided into logical stages.

Supported stages

```
Planning

Reconnaissance

Technology Discovery

Content Discovery

Scanning

Validation

Reporting
```

Additional stages MAY be introduced.

---

# Tasks

The plan SHALL reference Tasks.

```yaml
tasks:

- task_id
- task_id
- task_id
```

The Execution Plan SHALL NOT embed Task definitions.

---

# Dependency Graph

Task dependencies SHALL be represented.

```yaml
dependencies:

- source_task:

  target_task:

  relationship:
```

Supported relationships

```
Depends On

Blocks

Triggers
```

---

# Parallel Execution

The plan MAY define parallel execution groups.

Example

```yaml
parallel_groups:

- DNS

- TLS

- Port Scan
```

Tasks within the same group MAY execute concurrently.

---

# Sequential Execution

Tasks with dependencies SHALL execute sequentially.

Example

```
Technology Detection

↓

Content Discovery

↓

API Discovery
```

---

# Conditional Execution

Execution MAY depend on runtime discoveries.

Example

```yaml
condition:

Technology == "GraphQL"

↓

Execute GraphQL Agent
```

---

# Approval Gates

The plan SHALL identify tasks requiring approval.

```yaml
approval_gates:

task_id:

approval_type:
```

Execution SHALL pause until approval is granted.

---

# Retry Policy

The plan MAY define retry behavior.

```yaml
retry:

enabled:

max_attempts:

backoff_strategy:
```

Retry policy SHALL be interpreted by the Master Agent.

---

# Resource Constraints

The plan MAY define

```yaml
limits:

maximum_parallel_tasks:

maximum_request_rate:

maximum_runtime:
```

---

# Scheduling Strategy

Supported strategies

```
Sequential

Parallel

Adaptive

Hybrid
```

Adaptive scheduling SHOULD be preferred.

---

# Dynamic Replanning

Execution Plans MAY evolve.

Allowed triggers include

- New Technology
- New Host
- New Endpoint
- Scope Change
- Agent Failure
- Human Decision

Every change SHALL be versioned.

---

# Version History

Execution Plan revisions SHOULD record

```yaml
revision:

modified_by:

modified_at:

reason:
```

---

# Success Criteria

The plan MAY define completion conditions.

Examples

- All mandatory tasks completed
- No pending approval
- No unresolved critical failures
- Report generation initiated

---

# Validation Rules

A valid Execution Plan SHALL contain

- Execution Plan ID
- Assessment ID
- At least one Stage
- At least one Task
- Dependency graph
- Schema Version

---

# Quality Requirements

An Execution Plan SHALL

✓ Define execution stages

✓ Reference Tasks

✓ Define dependencies

✓ Support parallel execution

✓ Support conditional execution

✓ Support approval gates

✓ Support dynamic replanning

---

# Future Extensions

Future versions MAY include

- Cost estimation
- Resource optimization
- Distributed execution
- AI-assisted scheduling
- Risk-aware prioritization
- Calendar-aware execution windows

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Execution Plan provides a complete, adaptive, and auditable blueprint for executing a penetration testing assessment.

It SHALL be the authoritative source for task orchestration throughout the assessment lifecycle.