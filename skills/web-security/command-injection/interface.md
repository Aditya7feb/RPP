# Command Injection Interface

**File:** `skills/web-security/command-injection/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the
Command Injection Skill. Consumers depend only on this contract.

---

# Interface Overview

```
assess_command_injection(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: assess_command_injection

## Request

```yaml
target:

assets:

payload_set_ref:

collector_ref:

scope_id:

roe_id:

assessment_id:
```

- `target` (required) — an in-scope web application or API base URL.
- `assets` (optional) — the `web-application`, `endpoint`, and `api`
  [Assets](../../../schemas/asset.md) under test.
- `payload_set_ref` (optional) — a reference to a managed set of bounded probes. It
  SHALL be a reference, never inline destructive commands.
- `collector_ref` (optional) — a reference to a controlled out-of-band collector.
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
- `evidence` — [Evidence](../../../schemas/evidence.md) references.
- `status` — one of `completed`, `partial`, `denied`, `awaiting_approval`,
  `error`.
- `metrics` — counters such as injection points tested and findings emitted.

---

# Behavioral Contract

The skill SHALL

- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action and proceed only on `allow`
- Honor the attached rate ceiling
- Inject bounded probes and observe signals through the shared HTTP Client
- Bound time-based probe delays and never run harmful commands
- Record Observations and promote Evidence
- Emit Findings only with supporting Evidence
- Return `denied` when policy denies the required actions and
  `awaiting_approval` when approval is pending

The skill SHALL NOT

- Perform HTTP input or output directly
- Run harmful commands or alter the system
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
