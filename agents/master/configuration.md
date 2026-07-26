# Master Agent Configuration

**File:** `agents/master/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration that governs Master Agent
orchestration: scheduling policy, approval gating, retry policy, and Rules of
Engagement binding. Configuration is declarative and references canonical
schemas; it contains no capability logic.

---

# Configuration Precedence

Rules of Engagement override every orchestration decision. Precedence, highest
first:

1. [rules-of-engagement](../../schemas/rules-of-engagement.md)
2. [scope](../../schemas/scope.md)
3. Approval policy (this document)
4. Scheduling policy (this document)
5. Default orchestration behavior

A lower-precedence setting SHALL NEVER relax a higher-precedence constraint.

---

# Rules of Engagement Binding

The Master Agent SHALL enforce, on every delegation:

- Allowed hosts, ports, and protocols
- Authentication boundaries
- Excluded paths
- Request-rate limits
- Read-only validation constraints
- Human approval gates

No specialist tier agent may bypass these constraints.

---

# Scheduling Policy

The Master Agent SHALL schedule work according to:

1. Dependencies
2. Scope
3. Expected confidence gain
4. Cost
5. Runtime
6. Coverage

Independent work SHALL execute in parallel where dependencies and RoE permit.
Dependent work SHALL execute sequentially. Discovery SHALL precede capability
execution; reporting SHALL follow capability execution.

---

# Approval Gating Policy

The following classes of action SHALL require an approved
[approval](../../schemas/approval.md) object before delegation, regardless of
confidence:

- Authentication bypass, session manipulation, account-takeover, or MFA-bypass
  validation
- Injection validation (SQL, NoSQL, command, LDAP, template, XML external
  entity)
- Server-side request forgery and insecure-deserialization validation
- File-upload and path-traversal validation
- Any payload-driven active-testing action that changes target state

Without approval, the assessment SHALL stop at identification and SHALL NOT
attempt validation.

Approval states are owned by the [approval](../../schemas/approval.md) schema:
`NOT_REQUIRED`, `PENDING`, `APPROVED`, `REJECTED`, `EXPIRED`, `CANCELLED`.

---

# Retry Policy

The Master Agent MAY retry a delegated task only for transient orchestration
faults:

- Delegation transport timeout
- Temporary infrastructure unavailability
- Specialist agent crash
- Resource exhaustion

The Master Agent SHALL NOT retry on:

- Scope violation
- Permission denied
- Target actively blocking requests
- Approval rejected or expired

Retry backoff and limits reference [retry-policy](../../schemas/retry-policy.md).

---

# Completion Policy

The assessment SHALL be marked complete only when all mandatory phases have
completed, no runnable work remains, all approvals are resolved, and the
reporting pipeline has produced its outputs. Quality gates are validated at each
phase transition (see [execution.md](execution.md)).

---

# Extension Points

New capability tiers MAY be registered without changing this configuration.
Scheduling, approval, and retry policies apply uniformly to any compliant
specialist tier agent.
