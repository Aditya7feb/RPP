# Master Agent Examples

**File:** `agents/master/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of Master Agent
orchestration. All examples target capabilities, bind to canonical schemas, and
consume Findings, Evidence, and Risk by reference only.

---

# Example 1 — Capability-Oriented Delegation

The Master Agent requires TLS posture analysis. It routes the required capability
to the owning specialist tier agent, never to a tool.

```yaml
task:
  id: task-web-4210
  capability: web-security.tls-analysis
  target: asset-host-2001
  scope_ref: scope-eng-77
  roe_ref: roe-eng-77
  inputs:
    observation_refs:
      - observation-3300
```

The Web Security Agent coordinates its tier and returns references only.

```yaml
agent-response:
  task_ref: task-web-4210
  status: completed
  observation_refs:
    - observation-3401
  evidence_refs:
    - evidence-http-5501
  finding_refs:
    - finding-9007
  next_recommended:
    - web-security.security-headers
```

The Master Agent records `finding-9007` by reference and updates execution
state. It does not read or modify the finding's contents.

---

# Example 2 — Approval-Gated Active Validation

A candidate injection finding requires validation. The Master Agent gates it.

```yaml
approval:
  id: approval-6120
  finding_ref: finding-9007
  requested_action: active-testing.injection-validation
  state: PENDING
```

Only after the approval reaches `APPROVED` does the Master Agent delegate:

```yaml
task:
  id: task-at-6121
  capability: active-testing.injection-validation
  target: asset-endpoint-4110
  approval_ref: approval-6120
  scope_ref: scope-eng-77
  roe_ref: roe-eng-77
  inputs:
    finding_refs:
      - finding-9007
```

If the approval is `REJECTED` or `EXPIRED`, the assessment stops at
identification for that candidate and no validation is dispatched.

---

# Example 3 — Reporting Pipeline Orchestration

At the reporting phase the Master Agent invokes Reporting capabilities in order,
consuming each output by reference.

```yaml
execution_plan:
  phase: REPORTING
  steps:
    - capability: reporting.finding-correlation
      inputs: { finding_refs: [finding-9007, finding-9011] }
    - capability: reporting.risk-analysis
      inputs: { correlated_ref: correlation-2200 }
    - capability: reporting.report-generation
      inputs: { analysis_ref: analysis-3300 }
    - capability: reporting.evidence-bundle
      inputs: { evidence_refs: [evidence-http-5501] }
```

The Master Agent performs no deduplication, correlation, scoring, or rendering;
each is owned by the invoked Reporting capability. Canonical Risk remains owned
by the Domain Security tiers.

---

# Example 4 — Parallel Scheduling Under RoE

Discovery produced independent capability opportunities. The Master Agent
schedules non-conflicting work in parallel where RoE permits.

```yaml
execution_plan:
  phase: CAPABILITY EXECUTION
  parallel_groups:
    - - capability: authentication.session-analysis
        target: asset-web-application-1000
      - capability: web-security.security-headers
        target: asset-web-application-1000
      - capability: api-security.rest
        target: asset-api-1500
```

Dependent work (for example, active testing) is not placed in a parallel group
and is gated separately.

---

# Example 5 — Orchestration Error Handling

A delegated task times out. The Master Agent applies its retry policy and
continues independent work; it never fabricates results.

```yaml
execution_state:
  task_ref: task-cloud-7001
  outcome: delegation-timeout
  action: retry
  independent_work_continued: true
```

If retries are exhausted, the category becomes a recorded coverage gap and the
reporting pipeline is informed by reference.
