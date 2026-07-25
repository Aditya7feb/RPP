# Recon Interface

**File:** `skills/discovery/recon/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the Recon
Skill. Consumers depend only on this contract.

---

# Interface Overview

```
run_recon(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: run_recon

## Request

```yaml
scope_id:

roe_id:

targets:

profile:

assessment_id:
```

- `scope_id` (required) — the assessment [Scope](../../../schemas/scope.md).
- `roe_id` (required) — the
  [Rules of Engagement](../../../schemas/rules-of-engagement.md).
- `targets` (required) — seed in-scope targets.
- `profile` (optional) — the reconnaissance profile selecting phases and skills.
- `assessment_id` (optional) — correlating assessment identifier.

---

## Result

```yaml
assets:

relationships:

findings:

observations:

evidence:

workflow_ref:

status:

metrics:
```

- `assets` — the consolidated [Assets](../../../schemas/asset.md) from composed
  skills, reconciled by Asset Discovery.
- `relationships` — reconciled
  [Asset Relationships](../../../schemas/asset-relationship.md).
- `findings` — aggregated [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md).
- `observations` — orchestration and skill
  [Observations](../../../schemas/observation.md).
- `evidence` — aggregated [Evidence](../../../schemas/evidence.md) references.
- `workflow_ref` — the executed
  [Workflow Definition](../../../schemas/workflow-definition.md) reference.
- `status` — one of `completed`, `partial`, `awaiting_approval`, `denied`,
  `error`.
- `metrics` — counters such as phases executed and approvals requested.

---

# Behavioral Contract

The skill SHALL

- Build a Workflow Definition ordering the Discovery skills into phases
- Request phase authorization from the
  [Policy Engine](../../shared/policy-engine/README.md)
- Insert an approval gate before every active phase
- Drive the workflow through the
  [Workflow Runtime](../../shared/workflow-runtime/README.md)
- Invoke [Asset Discovery](../asset-discovery/README.md) to consolidate the graph
- Aggregate Findings, Observations, and Evidence
- Return `awaiting_approval` when an active phase requires approval

The skill SHALL NOT

- Probe any target directly
- Reimplement a composed skill
- Grant approvals itself

---

# Error Semantics

Errors are reported per the [error model](error-model.md). A denied phase yields
`denied`. A pending approval yields `awaiting_approval`. A failed step yields
`partial` with aggregated Evidence.

---

# Interface Stability

This interface is stable within the `1.x` series. Backward-compatible additions
MAY introduce new optional request fields and result counters. Breaking changes
SHALL increment the major version.

---

# Related Documents

- [Capabilities](capabilities.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Runtime Interface](../../shared/workflow-runtime/interface.md)
