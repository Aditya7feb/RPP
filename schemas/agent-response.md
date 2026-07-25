# Agent Response Schema

**File:** `schemas/agent-response.md`

**Version:** 1.0.0

---

# Purpose

The Agent Response Schema defines the canonical response format used by every agent within the Robust PenTest Platform (RPP).

Regardless of implementation, language, framework, or execution environment, every agent SHALL return responses conforming to this schema.

The schema enables consistent orchestration, auditing, planning, reporting, and recovery.

---

# Design Principles

An Agent Response SHALL be

- Deterministic
- Structured
- Machine-readable
- Human-readable
- Versioned
- Traceable
- Extensible

The response SHALL describe what the agent attempted, what it accomplished, and what should happen next.

---

# Relationship

```
Master Agent
      │
      │ Task
      ▼
Agent
      │
      ▼
Agent Response
      │
      ├── Findings
      ├── Evidence
      ├── Technologies
      ├── Metrics
      ├── Recommendations
      └── Errors
```

---

# Identity

Every Agent Response SHALL contain

```yaml
response_id:

assessment_id:

task_id:

agent_name:

schema_version:
```

---

# Execution Metadata

Every response SHALL record

```yaml
started_at:

completed_at:

duration:

execution_id:
```

---

# Status

Supported values

```
Success

Partial Success

Failed

Cancelled

Skipped

Waiting For Approval
```

Status SHALL represent the outcome of the assigned task.

---

# Summary

Every response SHALL include

```yaml
summary:

description:
```

The summary SHOULD provide a concise explanation of the completed work.

---

# Findings

Agents MAY return

```yaml
findings:

- finding_id
- finding_id
```

Findings SHALL reference Finding objects.

The response SHALL NOT embed full Finding definitions.

---

# Evidence

Agents MAY return

```yaml
evidence:

- evidence_id
- evidence_id
```

Evidence SHALL reference Evidence objects.

---

# Technologies

Agents MAY return

```yaml
technologies:

- technology_id
- technology_id
```

Technology detection SHOULD be reported whenever applicable.

---

# Produced Artifacts

Agents MAY generate

```yaml
artifacts:

reports:

logs:

screenshots:

pcaps:

exports:
```

Artifacts SHOULD reference external storage locations.

---

# Recommendations

Agents MAY recommend additional work.

```yaml
recommended_tasks:

- task_id

recommended_agents:

- agent_name

reason:
```

Example

```
Detected GraphQL Endpoint

↓

Recommend GraphQL Scanner
```

---

# Runtime Metrics

Every response SHOULD include

```yaml
metrics:

requests_sent:

requests_failed:

hosts_scanned:

ports_scanned:

endpoints_discovered:

files_discovered:
```

Implementations MAY expose additional metrics.

---

# Confidence

The response SHALL define

```yaml
confidence:

confidence_reason:
```

Confidence SHALL follow the Master Agent Confidence Model.

---

# Errors

Errors SHALL be structured.

```yaml
errors:

- severity:

  component:

  message:

  recoverable:
```

Supported severities

```
Info

Warning

Error

Critical
```

---

# Warnings

Agents MAY report

```yaml
warnings:

- description

- recommendation
```

Warnings SHALL NOT fail execution.

---

# Approval Requests

Agents MAY request approval.

```yaml
approval_required:

approval_type:

reason:
```

The Master Agent SHALL suspend dependent tasks until approval is resolved.

---

# Resource Usage

Agents SHOULD report

```yaml
resources:

cpu_time:

memory:

disk:

network_requests:
```

---

# Dependencies

Agents MAY identify newly discovered dependencies.

```yaml
new_dependencies:

- task_id

- technology_id
```

These MAY trigger dynamic replanning.

---

# Retry Recommendation

Agents MAY recommend retries.

```yaml
retry:

recommended:

reason:

suggested_delay:
```

The Master Agent SHALL decide whether to retry.

---

# Audit Information

Every response SHALL include

```yaml
generated_by:

agent_version:

execution_environment:

hostname:
```

---

# Validation Rules

A valid Agent Response SHALL contain

- Response ID
- Assessment ID
- Task ID
- Agent Name
- Status
- Execution Metadata
- Summary
- Schema Version

---

# Quality Requirements

An Agent Response SHALL

✓ Describe completed work

✓ Reference generated Findings

✓ Reference collected Evidence

✓ Report runtime metrics

✓ Record execution metadata

✓ Support auditability

✓ Enable adaptive planning

---

# Future Extensions

Future versions MAY include

- Token usage
- AI reasoning metadata
- Cost estimation
- Performance benchmarks
- Distributed execution metadata
- Agent capability negotiation
- Digital signatures

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Agent Response provides a complete, standardized description of an agent's execution, outputs, observations, and recommendations.

It SHALL serve as the primary communication contract between all agents and the Master Agent, enabling consistent orchestration, monitoring, and reporting across the platform.