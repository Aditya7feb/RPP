# Recon Error Model

**File:** `skills/discovery/recon/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Recon Skill and their
mapping to outcomes. Errors are classified deterministically so consumers can
respond consistently.

---

# Error Categories

```
Validation Error

Phase Authorization Denied

Awaiting Approval

Skill Step Error

Workflow Error

Internal Error
```

---

# Validation Error

Raised when the request is malformed — for example, missing `scope_id`, `roe_id`,
or `targets`, or a reference to a non-existent skill.

- Outcome — `error`
- Action — reject before building the workflow
- Evidence — none required

---

# Phase Authorization Denied

Raised when the [Policy Engine](../../shared/policy-engine/README.md) denies a
phase.

- Outcome — `denied`
- Action — halt per `stop_on_denied_phase`; fail closed for the denied phase
- Evidence — the policy decision reference

---

# Awaiting Approval

Raised when an active phase requires approval that has not yet been granted.

- Outcome — `awaiting_approval`
- Action — pause the workflow; resume only on approval
- Evidence — the approval request reference

---

# Skill Step Error

Raised when a composed Discovery skill step fails.

- Outcome — `partial`
- Action — continue with remaining steps where `continue_on_step_error` is
  enabled; record the failure
- Evidence — the composed skill's evidence where available

---

# Workflow Error

Raised when the [Workflow Runtime](../../shared/workflow-runtime/README.md) cannot
drive the workflow.

- Outcome — `error`
- Action — abort safely; preserve aggregated Evidence
- Evidence — the workflow diagnostic reference

---

# Internal Error

Raised for unexpected conditions within the skill.

- Outcome — `error`
- Action — abort safely
- Evidence — diagnostic context, redacted

---

# Outcome Mapping

| Category | Outcome | Fails Closed | Evidence |
|----------|---------|--------------|----------|
| Validation Error | error | Yes | No |
| Phase Authorization Denied | denied | Yes | Decision ref |
| Awaiting Approval | awaiting_approval | Yes (until approved) | Approval ref |
| Skill Step Error | partial | No | Skill evidence |
| Workflow Error | error | Yes | Workflow ref |
| Internal Error | error | Yes | Diagnostic |

---

# Error Handling Principles

The skill SHALL

- Fail closed on validation, authorization, workflow, and internal errors
- Never begin an active phase before its approval gate is satisfied
- Continue past a failed skill step only where configured
- Preserve all aggregated Evidence
- Never weaken the policy constraints of any composed skill
- Redact sensitive content in all error evidence

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Core Error Handling](../../core/error-handling.md)
- [Workflow Runtime Error Model](../../shared/workflow-runtime/error-model.md)
