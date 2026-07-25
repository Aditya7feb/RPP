# Session Management Execution Model

**File:** `skills/authentication/sessions/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Session Management
Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Observe Session Issuance (HTTP Client)

↓

Reach Authenticated State (managed credentials)

↓

Analyze Cookies And Session Lifecycle

↓

Record Observations → Evidence

↓

Analyze For Weaknesses

↓

Emit Findings And Risk

↓

Return Result
```

---

# Stage 1 — Validate Request

The skill SHALL validate that `target`, `scope_id`, and `roe_id` are present and
well formed. Invalid requests SHALL fail closed with a validation error and no
action.

---

# Stage 2 — Authorize

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action. Session testing is an `active` action. Only an
`allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Observe Session Issuance

The skill SHALL observe how session identifiers are issued through the
[HTTP Client](../../shared/http-client/README.md), capturing the canonical
[HTTP Session](../../../schemas/http-session.md) and
[HTTP Cookie](../../../schemas/http-cookie.md) representations. The skill SHALL NOT
perform requests directly.

---

# Stage 4 — Reach Authenticated State

Where managed credentials are provided, the skill SHALL reach a post-authentication
session state to evaluate identifier rotation and invalidation. Credentials SHALL
be referenced, never inlined, and never persisted in evidence.

---

# Stage 5 — Analyze Cookies And Session Lifecycle

The skill SHALL analyze cookie attributes, transport security, identifier entropy,
rotation after authentication, and invalidation on logout and timeout, using
deterministic criteria.

---

# Stage 6 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Session identifiers and secrets SHALL
be redacted.

---

# Stage 7 — Analyze For Weaknesses

The skill SHALL analyze the observations for session-management weaknesses using
deterministic criteria. Analysis SHALL be separate from observation.

---

# Stage 8 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 9 — Return Result

The skill SHALL return findings, observations, evidence, optional identities, a
`status`, and metrics per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from observation.
- All randomness, if any, SHALL be seeded and recorded.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial results SHALL
be returned with Evidence where available. Policy denial SHALL always fail closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Session Schema](../../../schemas/http-session.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
