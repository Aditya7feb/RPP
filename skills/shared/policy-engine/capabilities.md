# Policy Engine Capabilities

**File:** `skills/shared/policy-engine/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Policy Engine Shared
Skill. Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Policy Engine Interface](interface.md).

---

# Capability Model

```
Resolution

Scope Evaluation

Rules-of-Engagement Evaluation

Approval Determination

Ceiling Composition

Observability
```

---

# Resolution Capabilities

## Policy Resolution

The Policy Engine SHALL resolve the applicable
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md) for an assessment.

---

# Scope Evaluation Capabilities

## Target Scope Evaluation

The Policy Engine SHALL evaluate whether a target is `in_scope`,
`out_of_scope`, or `unknown`.

---

## Deny Out Of Scope

The Policy Engine SHALL deny any action against an out-of-scope target.

---

## Deny On Unknown

The Policy Engine SHALL deny by default when scope disposition is `unknown`.

---

# Rules-of-Engagement Evaluation Capabilities

## Action Permission Evaluation

The Policy Engine SHALL evaluate a proposed action against the Rules-of-Engagement
permissions and action classes.

---

## Prohibited Action Enforcement

The Policy Engine SHALL deny any action listed in `prohibited_actions`.

---

## Maintenance-Window Enforcement

The Policy Engine SHALL deny active and intrusive actions outside a required
maintenance window.

---

# Approval Determination Capabilities

## Approval Requirement Detection

The Policy Engine SHALL determine when an [Approval](../../../schemas/approval.md)
is required and return `requires_approval`.

---

## Non-Granting

The Policy Engine SHALL determine that approval is required but SHALL NOT grant
it.

---

# Ceiling Composition Capabilities

## Rate Ceiling Attachment

The Policy Engine SHALL attach the Rules-of-Engagement
[Rate Limit Policy](../../../schemas/rate-limit-policy.md) ceiling to allow
decisions.

---

# Observability Capabilities

## Decision Recording

The Policy Engine SHOULD record each decision as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

---

## Event Emission

The Policy Engine SHOULD publish decision events to the Execution State.

---

## Metrics

The Policy Engine SHOULD expose metrics including allowed, denied,
approval-required, and out-of-scope decision counts.

---

# Capability Boundaries

The Policy Engine SHALL NOT

- Execute actions
- Grant approvals
- Enforce rate limits directly
- Produce findings
- Perform target-facing operations

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Policy Resolution | Resolution | SHALL |
| Target Scope Evaluation | Scope Evaluation | SHALL |
| Deny Out Of Scope | Scope Evaluation | SHALL |
| Deny On Unknown | Scope Evaluation | SHALL |
| Action Permission Evaluation | RoE Evaluation | SHALL |
| Prohibited Action Enforcement | RoE Evaluation | SHALL |
| Maintenance-Window Enforcement | RoE Evaluation | SHALL |
| Approval Requirement Detection | Approval Determination | SHALL |
| Non-Granting | Approval Determination | SHALL |
| Rate Ceiling Attachment | Ceiling Composition | SHALL |
| Decision Recording | Observability | SHOULD |
| Event Emission | Observability | SHOULD |
| Metrics | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
