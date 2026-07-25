# Workflow Runtime Examples

**File:** `skills/shared/workflow-runtime/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Workflow Runtime Shared Skill in use.

Examples demonstrate plan execution, dependency scheduling, approval gating,
policy application, error behavior, resumption, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Executing A Baseline Web Workflow

The Master Agent executes a resolved plan derived from the `web-app-baseline`
workflow.

## Invocation

```yaml
metadata:
  request_id: req-7001
  assessment_id: asmt-42
execution_plan_id: plan-asmt-42-web-baseline
parameters:
  target: https://app.example.com
  max_depth: 2
mode: run
```

## Result

```yaml
outcome: completed
state_ref: state-asmt-42-web-baseline
step_summaries:
  - step_id: resolve-dns
    status: completed
  - step_id: probe-tls
    status: completed
  - step_id: discover-content
    status: completed
metrics:
  steps_completed: 3
  steps_failed: 0
```

Steps execute in dependency order and complete successfully.

---

# Example 2 — Dependency Scheduling

Steps run only after their dependencies complete.

```
resolve-dns (no deps)      → runs first

probe-tls (depends resolve-dns)   → runs after resolve-dns

discover-content (depends probe-tls) → runs after probe-tls
```

Independent steps in a wider plan MAY run concurrently, bounded by
`max_concurrency`.

---

# Example 3 — Approval Gate

An approval gate precedes the intrusive `discover-content` step.

## Result When Approval Pending

```yaml
outcome: awaiting_approval
state_ref: state-asmt-42-web-baseline
pending_approvals:
  - before: discover-content
    approval_ref: approval-active-scan
```

Execution pauses with durable state. Once the
[Approval](../../../schemas/approval.md) is granted, execution resumes and
dispatches the gated step.

---

# Example 4 — Policy Application

The runtime applies rate-limit and proxy policies to step traffic.

## Applied Policies

```yaml
step: discover-content
policies:
  rate_limit: ratelimitpolicy-default-http
  retry: retrypolicy-default-network
  proxy: proxy-corporate-egress
```

All requests issued by the step are paced by the
[Rate Limiter](../rate-limiter/README.md), retried by the
[Retry](../retry/README.md) shared skill, and routed by the
[Proxy](../proxy/README.md) shared skill.

---

# Example 5 — Error Behavior

A non-critical step fails with `on_error: continue`.

## Definition

```yaml
step_id: probe-optional-headers
on_error: continue
```

## Result

```yaml
step_summaries:
  - step_id: probe-optional-headers
    status: failed
outcome: completed
```

The workflow proceeds despite the failed optional step.

---

# Example 6 — Dry Run

A dry run validates and schedules without dispatching intrusive steps.

## Invocation

```yaml
mode: dry_run
execution_plan_id: plan-asmt-42-web-baseline
```

## Result

```yaml
outcome: completed
step_summaries:
  - step_id: resolve-dns
    status: completed
  - step_id: discover-content
    status: skipped   # intrusive, not dispatched in dry_run
```

Intrusive steps are validated but not executed.

---

# Example 7 — Resumption

An interrupted workflow resumes from durable state.

## Invocation

```yaml
mode: resume
resume_from_state: state-asmt-42-web-baseline
```

## Behavior

```
resolve-dns (completed)   → not re-run

probe-tls (completed)     → not re-run

discover-content (pending) → dispatched
```

Completed idempotent steps are not re-executed; execution continues from the
pending step.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
- [Execution Plan Schema](../../../schemas/execution-plan.md)
- [Execution State Schema](../../../schemas/execution-state.md)
