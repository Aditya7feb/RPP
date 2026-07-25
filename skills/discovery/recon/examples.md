# Recon Examples

**File:** `skills/discovery/recon/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Recon Skill.
Examples illustrate the interface and outputs; they contain no implementation code.

---

# Example 1 — Full Reconnaissance With Approval Gate

## Request

```yaml
scope_id: scope-example-2024
roe_id: roe-example-2024
targets:
  - example.com
profile: standard-web
```

## Result (passive phase complete, awaiting approval)

```yaml
assets:
  - id: asset-host-example-com
    type: host
    value: app.example.com
workflow_ref: workflow-recon-9001
status: awaiting_approval
observations:
  - id: obs-recon-4001
    kind: approval-requested
    phase: active
metrics:
  phases_executed: 1
  approvals_requested: 1
```

The passive phase completes and the workflow pauses at the approval gate before
the active phase.

---

# Example 2 — Active Phase Runs After Approval

## Continuation (after approval granted)

```yaml
assets:
  - id: asset-host-example-com
    type: host
    value: app.example.com
  - id: asset-service-443
    type: service
    value: tcp/443
relationships:
  - type: exposes
    from: asset-host-example-com
    to: asset-service-443
findings:
  - id: finding-recon-agg-01
    source_skill: tls-analysis
    risk_ref: risk-tls-3001
    evidence_refs:
      - evidence-tls-7001
workflow_ref: workflow-recon-9001
status: completed
metrics:
  phases_executed: 2
  skills_composed: 8
  findings_aggregated: 1
```

After approval, the active phase runs, Asset Discovery consolidates the graph, and
Findings from composed skills are aggregated with their Evidence.

---

# Example 3 — Passive-Only Profile

## Request

```yaml
scope_id: scope-example-2024
roe_id: roe-example-2024
targets:
  - example.com
profile: passive-only
```

## Result

```yaml
assets:
  - id: asset-domain-example-com
    type: domain
    value: example.com
findings: []
workflow_ref: workflow-recon-9002
status: completed
metrics:
  phases_executed: 1
  skills_composed: 2
```

A passive-only profile composes only passive skills; no approval gate for active
work is required because no active phase is scheduled.

---

# Example 4 — Denied Phase

## Request

```yaml
scope_id: scope-example-2024
roe_id: roe-example-2024
targets:
  - out-of-scope.example.net
profile: standard-web
```

## Result

```yaml
assets: []
findings: []
workflow_ref: workflow-recon-9003
status: denied
metrics:
  phases_executed: 0
  policy_denials: 1
```

The seed target is out of scope. The Policy Engine denies the phase and no
Discovery skills run.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Workflow Definition Schema](../../../schemas/workflow-definition.md)
