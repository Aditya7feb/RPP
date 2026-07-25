# Policy Engine Error Model

**File:** `skills/shared/policy-engine/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Policy Engine Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Policy Engine Shared Skill SHALL

- Produce canonical, structured errors
- Fail closed; never yield an implicit allow on error
- Preserve enough context for auditing
- Avoid leaking secrets

---

# Error Categories

The Policy Engine maps its failures onto the canonical categories.

```
Configuration

Validation

PolicyResolution

Evaluation

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid or incomplete.

Conditions

- `default_scope_id` references a missing Scope
- `default_roe_id` references a missing Rules of Engagement
- `fail_mode` is not `fail_closed`

Configuration errors SHALL be non-retryable and SHALL result in denial of the
requested action.

---

# Validation Errors

Raised when an action request is malformed.

Conditions

- Missing action class or intrusiveness
- Missing target
- Unrecognized action class

Validation errors SHALL be non-retryable and SHALL result in denial.

---

# Policy Resolution Errors

Raised when the applicable Scope or Rules of Engagement cannot be resolved.

Conditions

- No scope or Rules of Engagement available for the assessment
- A referenced policy is invalid

Policy resolution errors SHALL fail closed, denying the action.

---

# Evaluation Errors

Raised when evaluation cannot complete deterministically.

Conditions

- Ambiguous or contradictory policy that cannot be resolved by precedence
- Missing `current_time` for maintenance-window evaluation

Evaluation errors SHALL fail closed, denying the action, and SHOULD be surfaced
for policy correction.

---

# Adapter Errors

Raised when an underlying policy store fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation and SHALL fail closed.

---

# Internal Errors

Raised for unexpected conditions within the Policy Engine.

Internal errors SHALL be treated as non-retryable, SHALL fail closed, and SHOULD
be reported for diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

scope_id:

roe_id:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the request MAY be attempted again after
correction.

Errors SHALL NOT contain secret material.

---

# Outcome Mapping

| Outcome | Category | Effect | Retryable |
|---------|----------|--------|-----------|
| missing_scope | Configuration | Deny | No |
| missing_roe | Configuration | Deny | No |
| fail_open_configured | Configuration | Deny + reject config | No |
| malformed_request | Validation | Deny | No |
| policy_unresolved | PolicyResolution | Deny | No |
| ambiguous_policy | Evaluation | Deny | After correction |
| missing_time | Evaluation | Deny | After correction |
| store_failure | Adapter | Deny | Policy dependent |
| unexpected | Internal | Deny | No |

---

# Fail-Closed Principle

Every error path SHALL result in denial or a canonical error, never an implicit
allow.

The Policy Engine SHALL treat the inability to prove that an action is permitted
as equivalent to the action not being permitted.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category and policy
references, and SHALL exclude secrets.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Rules of Engagement Schema](../../../schemas/rules-of-engagement.md)
