# Unrestricted File Upload Error Model

**File:** `skills/web-security/file-upload/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical error categories of the Unrestricted File Upload
Skill and their mapping to outcomes. Errors are classified deterministically so
consumers can respond consistently.

---

# Error Categories

```
Validation Error

Authorization Denied

Awaiting Approval

Upload Error

Transport Error

Rate Limited

Timeout

Internal Error
```

---

# Validation Error

Raised when the request is malformed — for example, a missing `target`,
`scope_id`, or `roe_id`.

- Outcome — `error`
- Action — reject before any testing
- Evidence — none required

---

# Authorization Denied

Raised when the [Policy Engine](../../shared/policy-engine/README.md) denies a
required action or the target is out of scope.

- Outcome — `denied`
- Action — halt the denied action; fail closed
- Evidence — the policy decision reference

---

# Awaiting Approval

Raised when a required action returns `requires_approval`, as upload testing commonly
does.

- Outcome — `awaiting_approval`
- Action — defer the action until approval is granted
- Evidence — the approval request reference

---

# Upload Error

Raised when a marker file cannot be delivered to a specific upload endpoint.

- Outcome — `partial`
- Action — continue with remaining endpoints; record the failure
- Evidence — the failed observation reference

---

# Transport Error

Raised when an HTTP interaction fails for a specific check.

- Outcome — `partial`
- Action — continue with remaining checks; record the failure
- Evidence — the failed observation reference

---

# Rate Limited

Raised when the policy rate ceiling or a self-imposed limit is reached.

- Outcome — `partial`
- Action — pace or defer remaining actions
- Evidence — the rate decision reference

---

# Timeout

Raised when an interaction exceeds the configured timeout.

- Outcome — `partial`
- Action — record and continue
- Evidence — timing observation where available

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
| Authorization Denied | denied | Yes | Decision ref |
| Awaiting Approval | awaiting_approval | Yes | Approval ref |
| Upload Error | partial | No | Observation ref |
| Transport Error | partial | No | Observation ref |
| Rate Limited | partial | No | Decision ref |
| Timeout | partial | No | Timing ref |
| Internal Error | error | Yes | Diagnostic |

---

# Error Handling Principles

The skill SHALL

- Fail closed on validation, authorization, and internal errors
- Return partial results with Evidence where safe
- Never emit a Finding without supporting Evidence
- Never upload functional malicious payloads in response to an error
- Never weaken policy constraints in response to an error
- Redact sensitive content in all error evidence

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Configuration](configuration.md)
- [Core Error Handling](../../core/error-handling.md)
- [Policy Engine Error Model](../../shared/policy-engine/error-model.md)
