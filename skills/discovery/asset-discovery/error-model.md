# Asset Discovery Error Model

**File:** `skills/discovery/asset-discovery/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Asset Discovery Skill
and their mapping to outcomes. Errors are classified deterministically so consumers
can respond consistently.

---

# Error Categories

```
Validation Error

Scope Confirmation Error

Merge Conflict

Relationship Inconsistency

Internal Error
```

---

# Validation Error

Raised when the request is malformed — for example, missing `assets`, `scope_id`,
or `roe_id`, or a non-canonical Asset.

- Outcome — `error`
- Action — reject before any consolidation
- Evidence — none required

---

# Scope Confirmation Error

Raised when the [Policy Engine](../../shared/policy-engine/README.md) cannot
confirm the scope of an Asset.

- Outcome — `partial`
- Action — exclude the unconfirmable Asset from the in-scope graph; flag it
- Evidence — the policy decision reference

---

# Merge Conflict

Raised when duplicate Assets carry conflicting facts.

- Outcome — `partial`
- Action — handle per the configured conflict policy; flag conflicts; never
  silently discard
- Evidence — the conflicting observation references

---

# Relationship Inconsistency

Raised when a relationship references a missing Asset endpoint.

- Outcome — `partial`
- Action — flag or drop per configuration; record the inconsistency
- Evidence — the relationship reference

---

# Internal Error

Raised for unexpected conditions within the skill.

- Outcome — `error`
- Action — abort safely; emit no partial Findings without Evidence
- Evidence — diagnostic context, redacted

---

# Outcome Mapping

| Category | Outcome | Fails Closed | Evidence |
|----------|---------|--------------|----------|
| Validation Error | error | Yes | No |
| Scope Confirmation Error | partial | Yes (excludes Asset) | Decision ref |
| Merge Conflict | partial | No | Observation refs |
| Relationship Inconsistency | partial | No | Relationship ref |
| Internal Error | error | Yes | Diagnostic |

---

# Error Handling Principles

The skill SHALL

- Fail closed on validation and internal errors
- Exclude Assets whose scope cannot be confirmed
- Never silently discard conflicting facts
- Never emit a Finding without supporting Evidence
- Never perform network activity in response to an error
- Redact sensitive content in all error evidence

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Core Error Handling](../../core/error-handling.md)
- [Policy Engine Error Model](../../shared/policy-engine/error-model.md)
