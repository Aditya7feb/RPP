# Policy Engine Interface

**File:** `skills/shared/policy-engine/interface.md`

**Version:** 1.0.0

---

# Purpose

The Policy Engine Interface defines the canonical contract through which platform
components obtain an authorization decision before acting against a target.

The interface standardizes the action request, the decision, and the decision
record while remaining independent of any implementation.

All consumers SHALL obtain authorization exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Deterministic
- Versioned
- Observable
- Backward Compatible
- Conservative By Default

---

# Relationship

```
Master Agent / Workflow Runtime / Domain Skill

↓

Policy Engine Interface

↓

Policy Engine Shared Skill

↓

Policy Decision
```

The interface SHALL NOT expose or depend on evaluation internals.

---

# Interface Overview

```
Metadata

↓

Action Request

↓

Policy References

↓

Execution Context

↓

Policy Decision

↓

Evidence

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Action Request

Every invocation SHALL define

```yaml
target:

asset_id:

action_class:

intrusiveness:

capability:
```

`target` SHALL identify the entity the action concerns.

`asset_id` MAY reference the [Asset](../../../schemas/asset.md) when established.

`action_class` SHALL be a canonical action class such as `discovery`,
`fingerprinting`, `validation`, `exploitation`, or `intrusive`.

`intrusiveness` SHALL be one of `passive`, `active`, or `intrusive`.

`capability` SHALL identify the requesting capability.

The interface SHALL NOT require the action payload.

---

# Policy References

Every invocation SHALL reference

```yaml
scope_id:

roe_id:
```

`scope_id` SHALL reference the applicable [Scope](../../../schemas/scope.md).

`roe_id` SHALL reference the applicable
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

Absent references SHALL resolve to the assessment defaults.

---

# Execution Context

The Policy Engine Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

current_time:

variables:
```

`current_time` SHALL be used for maintenance-window evaluation.

The interface SHALL treat context as read-only.

---

# Policy Decision

Every invocation SHALL return a normalized decision.

```yaml
decision:

justification:

approval_reference:

rate_ceiling_policy_id:

scope_status:

evidence:
```

`decision` SHALL be one of

```
allow

deny

requires_approval
```

`justification` SHALL explain the decision in terms of scope and Rules of
Engagement.

`approval_reference` SHALL be present when `decision` is `requires_approval`.

`rate_ceiling_policy_id` SHALL be present when `decision` is `allow`.

`scope_status` SHALL report the evaluated target disposition.

---

# Evidence

The interface SHALL expose a structured decision record.

Evidence MAY include

- The action request
- Scope and Rules-of-Engagement evaluation results
- The final decision and justification

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Policy Engine error model](error-model.md).

When policy cannot be resolved, the interface SHALL fail closed with a `deny`
outcome or a canonical configuration error, never an implicit allow.

---

# Determinism

Given identical request, policy references, and `current_time`, the Policy Engine
SHALL return an identical decision.

---

# Compatibility

The interface SHALL remain stable across action classes and consumers.

Consumers SHALL require no modification when policy content changes.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Action Request with an action class and intrusiveness
- Policy References or resolvable defaults
- Execution Context including `current_time`
- Policy Decision
- Error Handling
- Evidence

---

# Quality Requirements

The Policy Engine Interface SHALL

✓ Remain implementation independent

✓ Produce a deterministic decision

✓ Fail closed

✓ Support structured errors

✓ Preserve decision evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Decision explanation traces
- Batch action evaluation
- Time-boxed grant handles

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Policy Engine Interface provides a stable, deterministic, and
implementation-independent contract through which every platform component
obtains an auditable authorization decision before acting across the Robust
PenTest Platform.
