# Recon Capabilities

**File:** `skills/discovery/recon/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Recon Skill. Capabilities
describe *what* the skill provides, not *how* it is implemented.

Each capability is implementation independent and consumed through the
[Recon Interface](interface.md).

---

# Capability Model

```
Workflow Composition

Phase Authorization

Approval Gating

Orchestration

Consolidation

Observability
```

---

# Workflow Composition Capabilities

## Workflow Definition Construction

The skill SHALL build a
[Workflow Definition](../../../schemas/workflow-definition.md) that orders the
Discovery skills into passive and active phases.

---

## Profile Selection

The skill SHALL select the composed skills and phases from a reconnaissance
profile.

---

# Phase Authorization Capabilities

## Phase Authorization

The skill SHALL request authorization from the
[Policy Engine](../../shared/policy-engine/README.md) before each phase.

---

## Scope Confinement

The skill SHALL confine all composed activity to the assessment
[Scope](../../../schemas/scope.md).

---

# Approval Gating Capabilities

## Active-Phase Approval Gate

The skill SHALL insert an approval gate before every active phase.

---

## Workflow Pause And Resume

The skill SHALL pause the workflow on a `requires_approval` decision and resume
only when approval is granted.

---

# Orchestration Capabilities

## Workflow Driving

The skill SHALL drive the workflow through the
[Workflow Runtime](../../shared/workflow-runtime/README.md).

---

## Step Composition

The skill SHALL compose Discovery skills as workflow steps without reimplementing
them.

---

# Consolidation Capabilities

## Asset Consolidation Invocation

The skill SHALL invoke [Asset Discovery](../asset-discovery/README.md) to
consolidate the produced asset graph.

---

## Result Aggregation

The skill SHALL aggregate [Findings](../../../schemas/finding.md),
[Observations](../../../schemas/observation.md), and
[Evidence](../../../schemas/evidence.md) from all composed skills.

---

# Observability Capabilities

## Orchestration Observations

The skill SHALL record [Observations](../../../schemas/observation.md) describing
phase execution and approvals.

---

## Event Emission

The skill SHOULD publish workflow lifecycle events to the Execution State.

---

## Metrics

The skill SHOULD expose metrics including phases executed, approvals requested, and
skills composed.

---

# Capability Boundaries

The skill SHALL NOT

- Probe, scan, resolve, or request any target directly
- Reimplement a composed skill
- Deduplicate Assets itself
- Grant approvals
- Produce vulnerability Findings itself

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Workflow Definition Construction | Workflow Composition | SHALL |
| Profile Selection | Workflow Composition | SHALL |
| Phase Authorization | Phase Authorization | SHALL |
| Scope Confinement | Phase Authorization | SHALL |
| Active-Phase Approval Gate | Approval Gating | SHALL |
| Workflow Pause And Resume | Approval Gating | SHALL |
| Workflow Driving | Orchestration | SHALL |
| Step Composition | Orchestration | SHALL |
| Asset Consolidation Invocation | Consolidation | SHALL |
| Result Aggregation | Consolidation | SHALL |
| Orchestration Observations | Observability | SHALL |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Runtime](../../shared/workflow-runtime/README.md)
