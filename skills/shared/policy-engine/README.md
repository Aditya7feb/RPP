# Policy Engine Shared Skill

**File:** `skills/shared/policy-engine/README.md`

**Version:** 1.0.0

---

# Purpose

The Policy Engine Shared Skill provides the canonical, implementation-independent
authorization gate that every capability within the Robust PenTest Platform (RPP)
SHALL consult before acting against a target.

Rather than allowing individual skills to interpret scope and Rules of Engagement
independently, this shared skill centralizes the decision of whether a proposed
action against an [Asset](../../../schemas/asset.md) is permitted, denied, or
requires approval.

The Policy Engine is the mandatory pre-action authorization gate. No intrusive
capability SHALL execute without an allow decision from the Policy Engine.

---

# Goals

The Policy Engine Shared Skill SHALL

- Provide a single authorization decision for any proposed action
- Evaluate the target against the assessment [Scope](../../../schemas/scope.md)
- Evaluate the action against the
  [Rules of Engagement](../../../schemas/rules-of-engagement.md)
- Determine when an [Approval](../../../schemas/approval.md) is required
- Compose operational ceilings such as rate limits into the decision
- Produce an auditable policy-decision record as evidence
- Integrate with platform observability

---

# Non-Goals

The Policy Engine Shared Skill SHALL NOT

- Execute the proposed action
- Detect vulnerabilities
- Produce security findings
- Perform target-facing operations
- Grant approvals; it SHALL determine when approval is required
- Enforce rate limits directly; it SHALL reference the ceiling and defer
  enforcement to the [Rate Limiter](../rate-limiter/README.md)

The Policy Engine decides *whether* an action is permitted. The caller owns
*how* the action executes, subject to the decision.

---

# Design Principles

The Policy Engine Shared Skill SHALL be

- Deterministic given the same inputs
- Conservative by default; deny when uncertain
- Scope and Rules-of-Engagement driven
- Auditable
- Observable
- Secure by default

---

# Architecture

```
Master Agent / Workflow Runtime / Domain Skill

↓

Policy Engine Shared Skill

├── Scope Evaluator
├── Rules-of-Engagement Evaluator
├── Approval Determiner
├── Ceiling Composer
├── Decision Recorder
├── Event Manager

↓

Policy Decision
```

The Policy Engine returns a decision. It SHALL remain unaware of how the action
is subsequently executed.

---

# Responsibilities

The Policy Engine Shared Skill is responsible for

- Resolving the applicable [Scope](../../../schemas/scope.md) and
  [Rules of Engagement](../../../schemas/rules-of-engagement.md)
- Evaluating an action request against target scope and permitted actions
- Determining whether an [Approval](../../../schemas/approval.md) is required
- Composing the Rules-of-Engagement rate ceiling into the decision
- Emitting an auditable policy-decision record
- Publishing decision events

---

# Decision Lifecycle

```
Receive Action Request

↓

Resolve Scope and Rules of Engagement

↓

Evaluate Target Scope

├── out_of_scope → Deny

└── in_scope
      ↓
      Evaluate Action Against RoE

      ├── prohibited → Deny
      ├── requires approval → Require Approval
      └── permitted → Allow (with ceilings)

↓

Record Decision and Emit Event
```

Every decision SHOULD be preserved as evidence.

---

# Action Request

An action request SHALL describe

- The target or [Asset](../../../schemas/asset.md)
- The proposed action class, such as `discovery`, `validation`, or
  `exploitation`
- The intrusiveness of the action
- The capability requesting the decision

The Policy Engine SHALL NOT require the action payload; it evaluates intent, not
content.

---

# Scope Evaluation

The Policy Engine SHALL evaluate the target against the assessment
[Scope](../../../schemas/scope.md).

A target that is `out_of_scope` SHALL be denied regardless of Rules of
Engagement.

Where scope disposition is `unknown`, the Policy Engine SHALL deny by default and
MAY require operator resolution.

---

# Rules-of-Engagement Evaluation

For in-scope targets, the Policy Engine SHALL evaluate the action against the
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

- Actions in `prohibited_actions` SHALL be denied
- Actions permitted by the relevant permission and action class SHALL be allowed
- Actions in `approval_required_for` SHALL require approval
- Active and intrusive actions outside a required maintenance window SHALL be
  denied

The most restrictive applicable rule SHALL govern.

---

# Approval Determination

Where Rules of Engagement require approval, the Policy Engine SHALL return a
`requires_approval` decision referencing the applicable
[Approval](../../../schemas/approval.md) requirement.

The Policy Engine SHALL determine that approval is required; it SHALL NOT grant
it. Granting is the responsibility of the master agent approval process.

---

# Ceiling Composition

For allow decisions, the Policy Engine SHALL compose the Rules-of-Engagement rate
ceiling, referencing the applicable
[Rate Limit Policy](../../../schemas/rate-limit-policy.md).

Enforcement of the ceiling SHALL be performed by the
[Rate Limiter](../rate-limiter/README.md); the Policy Engine only attaches the
ceiling to the decision.

---

# Decision Record

Every decision SHALL be recorded as evidence, including

- The action request
- The scope evaluation result
- The Rules-of-Engagement evaluation result
- The final decision and its justification

Decision records SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain secrets.

---

# Events

The Policy Engine Shared Skill SHOULD publish

- DecisionRequested
- ActionAllowed
- ActionDenied
- ApprovalRequired
- OutOfScopeRejected

Events SHALL integrate with the platform Execution State.

---

# Dependencies

The Policy Engine Shared Skill depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Scope Schema](../../../schemas/scope.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
- [Approval Schema](../../../schemas/approval.md)
- [Asset Schema](../../../schemas/asset.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
- [Evidence Schema](../../../schemas/evidence.md)

The Policy Engine Shared Skill SHALL NOT depend on domain skills or on any
package that performs target-facing input or output.

---

# Consumers

Every capability that acts against a target SHALL consult the Policy Engine,
including

- The [Workflow Runtime](../workflow-runtime/README.md) at step dispatch
- All Discovery, Authentication, Web Security, API, and Cloud skills
- The Master Agent before delegating intrusive work

---

# Outputs

Typical outputs MAY include

- A policy decision of `allow`, `deny`, or `requires_approval`
- An attached rate ceiling for allow decisions
- A decision evidence reference
- Policy metrics

Outputs SHALL remain implementation independent.

---

# Security Principles

The Policy Engine Shared Skill SHALL

- Deny by default when scope or permission is uncertain
- Enforce Rules of Engagement as an inviolable boundary
- Prevent any out-of-scope action
- Require approval for actions the Rules of Engagement gate
- Preserve an auditable trail of every decision

Acting without authorization can harm targets and violate engagement scope. The
Policy Engine SHALL make authorization explicit and mandatory.

---

# Best Practices

Consumers SHOULD

- Consult the Policy Engine before every target-facing action
- Pass the intended action class and intrusiveness accurately
- Honor `requires_approval` by routing to the approval process
- Attach the returned ceiling to outbound operations
- Capture decision evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Act against a target without a decision
- Interpret scope or Rules of Engagement independently
- Treat `requires_approval` as `allow`
- Bypass the Policy Engine for "read-only" probing without confirming it is
  permitted
- Persist secrets in decision records

---

# Documentation Requirements

This shared skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-policy-engine-authorization-gate.md

---

# Related Shared Packages

- [Rate Limiter](../rate-limiter/README.md)
- [Evidence](../evidence/README.md)
- [Workflow Runtime](../workflow-runtime/README.md)

---

# Canonical Schemas

- [Scope](../../../schemas/scope.md)
- [Rules of Engagement](../../../schemas/rules-of-engagement.md)
- [Approval](../../../schemas/approval.md)
- [Asset](../../../schemas/asset.md)
- [Evidence](../../../schemas/evidence.md)

---

# Architecture Decisions

- [ADR-001 — Policy Engine Authorization Gate](adr/ADR-001-policy-engine-authorization-gate.md)

---

# Future Extensions

Future versions MAY support

- Explanation traces for every decision
- Per-action-class policy overlays
- Delegated approval workflows
- Time-boxed action grants

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Policy Engine Shared Skill provides a deterministic, conservative,
and implementation-independent authorization gate for the Robust PenTest
Platform.

It enables every capability to obtain a single, auditable decision on whether a
proposed action is permitted, denied, or requires approval, enforcing Scope and
Rules of Engagement without embedding authorization logic in consumers.
