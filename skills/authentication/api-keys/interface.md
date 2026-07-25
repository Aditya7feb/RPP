# API Key Authentication Interface

**File:** `skills/authentication/api-keys/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the API
Key Authentication Skill. Consumers depend only on this contract.

---

# Interface Overview

```
assess_api_keys(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: assess_api_keys

## Request

```yaml
target:

assets:

api_key_ref:

scope_id:

roe_id:

assessment_id:
```

- `target` (required) — an in-scope API or application base URL.
- `assets` (optional) — the `api`, `endpoint`, and `web-application`
  [Assets](../../../schemas/asset.md) under test.
- `api_key_ref` (optional) — a reference to a managed test key. It SHALL be a
  reference, never an inline key.
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

status:

metrics:
```

- `findings` — [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md).
- `observations` — [Observations](../../../schemas/observation.md) recorded.
- `evidence` — [Evidence](../../../schemas/evidence.md) references, key material
  redacted.
- `status` — one of `completed`, `partial`, `denied`, `awaiting_approval`,
  `error`.
- `metrics` — counters such as checks performed and findings emitted.

---

# Behavioral Contract

The skill SHALL

- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action and proceed only on `allow`
- Honor the attached rate ceiling
- Observe API key handling through the shared HTTP Client
- Record Observations and promote Evidence with key material redacted
- Emit Findings only with supporting Evidence
- Return `denied` when policy denies the required actions and
  `awaiting_approval` when approval is pending

The skill SHALL NOT

- Perform HTTP input or output directly
- Persist key material
- Act on out-of-scope targets

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
