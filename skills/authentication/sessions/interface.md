# Session Management Interface

**File:** `skills/authentication/sessions/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the
Session Management Skill. Consumers depend only on this contract.

---

# Interface Overview

```
assess_sessions(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: assess_sessions

## Request

```yaml
target:

assets:

credentials_ref:

scope_id:

roe_id:

assessment_id:
```

- `target` (required) — an in-scope web application base URL.
- `assets` (optional) — the `web-application` and `endpoint`
  [Assets](../../../schemas/asset.md) under test.
- `credentials_ref` (optional) — a reference to managed test credentials. It SHALL
  be a reference, never inline secrets.
- `scope_id` (required) — the assessment [Scope](../../../schemas/scope.md).
- `roe_id` (required) — the
  [Rules of Engagement](../../../schemas/rules-of-engagement.md).
- `assessment_id` (optional) — correlating assessment identifier.

---

## Result

```yaml
findings:

observations:

evidence:

identities:

status:

metrics:
```

- `findings` — [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md).
- `observations` — [Observations](../../../schemas/observation.md) recorded.
- `evidence` — [Evidence](../../../schemas/evidence.md) references, secrets
  redacted.
- `identities` — optional `identity` [Assets](../../../schemas/asset.md) for
  confirmed authenticated contexts.
- `status` — one of `completed`, `partial`, `denied`, `awaiting_approval`,
  `error`.
- `metrics` — counters such as checks performed and findings emitted.

---

# Behavioral Contract

The skill SHALL

- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action and proceed only on `allow`
- Honor the attached rate ceiling
- Observe session behavior through the shared HTTP Client
- Record Observations and promote Evidence with secrets redacted
- Emit Findings only with supporting Evidence
- Return `denied` when policy denies the required actions and
  `awaiting_approval` when approval is pending

The skill SHALL NOT

- Perform HTTP input or output directly
- Persist session secrets
- Act on out-of-scope applications

---

# Error Semantics

Errors are reported per the [error model](error-model.md). Policy denial yields a
`denied` status; a pending approval yields `awaiting_approval`; transport failures
yield `partial` or `error` with Evidence where available.

---

# Interface Stability

This interface is stable within the `1.x` series. Backward-compatible additions
MAY introduce new optional request fields and result counters. Breaking changes
SHALL increment the major version.

---

# Related Documents

- [Capabilities](capabilities.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Policy Engine Interface](../../shared/policy-engine/interface.md)
