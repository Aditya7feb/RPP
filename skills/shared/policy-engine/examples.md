# Policy Engine Examples

**File:** `skills/shared/policy-engine/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Policy Engine Shared Skill in use.

Examples demonstrate allow, deny, out-of-scope, approval-required, maintenance
window, fail-closed, and evidence outcomes.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Allowed Passive Discovery

A discovery skill requests permission to passively resolve a subdomain.

## Invocation

```yaml
metadata:
  request_id: req-11001
  assessment_id: asmt-42
  task_id: task-subdomain
  skill_id: subdomain-discovery
target: api.example.com
action_class: discovery
intrusiveness: passive
capability: subdomain-discovery
scope_id: scope-asmt-42
roe_id: roe-asmt-42
```

## Decision

```yaml
decision: allow
scope_status: in_scope
justification: in-scope target; passive discovery permitted by Rules of Engagement
rate_ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

The action is permitted and a rate ceiling is attached for enforcement by the
[Rate Limiter](../rate-limiter/README.md).

---

# Example 2 — Out-Of-Scope Denied

An action targets a host outside the scope.

## Invocation

```yaml
target: status.example.com
action_class: discovery
intrusiveness: active
```

## Decision

```yaml
decision: deny
scope_status: out_of_scope
justification: target excluded by scope; action denied
```

No out-of-scope action is permitted regardless of Rules of Engagement.

---

# Example 3 — Prohibited Action Denied

An action class is prohibited by Rules of Engagement.

## Invocation

```yaml
target: app.example.com
action_class: denial-of-service
intrusiveness: intrusive
```

## Decision

```yaml
decision: deny
scope_status: in_scope
justification: action in prohibited_actions; denied
```

Prohibited actions override every permission.

---

# Example 4 — Approval Required

An exploitation action is gated by Rules of Engagement.

## Invocation

```yaml
target: app.example.com
action_class: exploitation
intrusiveness: intrusive
```

## Decision

```yaml
decision: requires_approval
scope_status: in_scope
approval_reference: approval-exploitation
justification: exploitation requires approval per Rules of Engagement
```

The consumer routes to the master agent approval process; it SHALL NOT treat this
as an allow.

---

# Example 5 — Outside Maintenance Window

An intrusive action is requested outside the permitted window.

## Context

```yaml
current_time: 2026-07-25T20:00:00Z
```

## Decision

```yaml
decision: deny
scope_status: in_scope
justification: intrusive action outside maintenance window; denied
```

Active and intrusive actions are denied outside a required maintenance window.

---

# Example 6 — Fail Closed On Unresolved Policy

The Rules of Engagement cannot be resolved.

## Decision

```yaml
decision: deny
error:
  category: PolicyResolution
  code: policy_unresolved
  retryable: false
```

The Policy Engine fails closed; inability to prove permission is treated as
denial.

---

# Example 7 — Decision Evidence Record

A single decision produces the following evidence.

```yaml
evidence:
  type: policy-decision
  target: api.example.com
  action_class: discovery
  intrusiveness: passive
  scope_status: in_scope
  decision: allow
  roe_id: roe-asmt-42
  scope_id: scope-asmt-42
  decided_at: 2026-07-25T19:00:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes secrets, and supports
auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
- [Scope Schema](../../../schemas/scope.md)
