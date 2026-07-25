# Policy Engine Execution Model

**File:** `skills/shared/policy-engine/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Policy Engine Shared Skill.

The execution model describes how the shared skill processes an action request
from policy resolution through scope and Rules-of-Engagement evaluation to a
final, auditable decision.

The model is deterministic given the same request, policy references, and time.

---

# Execution Overview

```
Receive Action Request

↓

Resolve Configuration and Policies

↓

Evaluate Target Scope

↓

Evaluate Action Against Rules of Engagement

↓

Determine Approval Requirement

↓

Compose Rate Ceiling (for allow)

↓

Record Decision and Emit Event

↓

Return Decision
```

---

# Stage 1 — Policy Resolution

The Policy Engine SHALL resolve the effective
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md) using the
precedence defined in [configuration.md](configuration.md).

If policy cannot be resolved, the Policy Engine SHALL fail closed with a
configuration error rather than allow the action.

---

# Stage 2 — Scope Evaluation

The Policy Engine SHALL evaluate the target against the Scope.

```
out_of_scope → Deny

unknown → Deny (or Require Approval per configuration)

in_scope → proceed
```

Scope evaluation SHALL be deterministic and SHALL precede Rules-of-Engagement
evaluation.

---

# Stage 3 — Rules-of-Engagement Evaluation

For in-scope targets, the Policy Engine SHALL evaluate the action.

```
action in prohibited_actions → Deny

active/intrusive outside maintenance window → Deny

permission or action class not granted → Deny

action in approval_required_for → Require Approval

otherwise → Allow
```

The most restrictive applicable rule SHALL govern.

---

# Stage 4 — Approval Determination

Where Rules of Engagement require approval, the Policy Engine SHALL return
`requires_approval` with a reference to the applicable
[Approval](../../../schemas/approval.md) requirement.

Where approval grants are cached and a valid grant exists for an identical
action, the Policy Engine MAY return `allow`, subject to Rules of Engagement.

The Policy Engine SHALL NOT grant approvals.

---

# Stage 5 — Ceiling Composition

For allow decisions, the Policy Engine SHALL attach the Rules-of-Engagement
[Rate Limit Policy](../../../schemas/rate-limit-policy.md) ceiling.

The Policy Engine SHALL NOT enforce the ceiling; enforcement is performed by the
[Rate Limiter](../rate-limiter/README.md) when the action executes.

---

# Stage 6 — Decision Recording

The Policy Engine SHALL record the decision, including the request, the scope and
Rules-of-Engagement results, and the justification, as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

Decision records SHALL exclude secrets.

---

# Stage 7 — Events

The Policy Engine SHOULD emit a decision event to the Execution State.

---

# Determinism

Given identical request, policy references, and `current_time`, the Policy Engine
SHALL return an identical decision and justification.

---

# Conservative Default

At every stage where the outcome is uncertain — unresolved policy, unknown scope,
or ambiguous permission — the Policy Engine SHALL deny or require approval, never
allow.

---

# Interaction With Other Components

- The [Workflow Runtime](../workflow-runtime/README.md) SHALL consult the Policy
  Engine before dispatching a step that acts against a target.
- Domain skills SHALL consult the Policy Engine before any target-facing action.
- The [Rate Limiter](../rate-limiter/README.md) SHALL enforce the ceiling
  attached to an allow decision.
- The master agent approval process SHALL resolve `requires_approval` decisions.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failure to resolve or evaluate policy SHALL result in a `deny` outcome or a
canonical error, never an implicit allow.

---

# Execution Outputs

The execution model SHALL produce

- A normalized policy decision
- An attached rate ceiling for allow decisions
- A decision evidence reference
- Policy metrics

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
- [Execution Model](../../core/execution-model.md)
