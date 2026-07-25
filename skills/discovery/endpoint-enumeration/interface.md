# Endpoint Enumeration Interface

**File:** `skills/discovery/endpoint-enumeration/interface.md`

**Version:** 1.0.0

---

# Purpose

This document defines the stable, implementation-independent interface of the
Endpoint Enumeration Skill. Consumers depend only on this contract.

---

# Interface Overview

```
enumerate_endpoints(request) → result
```

The skill exposes a single primary operation. Its behavior is governed by the
[configuration](configuration.md) and the [execution model](execution.md).

---

# Operation: enumerate_endpoints

## Request

```yaml
target:

seed_endpoints:

mine_parameters:

scope_id:

roe_id:

assessment_id:
```

- `target` (required) — an in-scope web application base URL.
- `seed_endpoints` (optional) — endpoints from other skills to enrich.
- `mine_parameters` (optional) — whether parameter mining is performed.
- `scope_id` (required) — the assessment [Scope](../../../schemas/scope.md).
- `roe_id` (required) — the
  [Rules of Engagement](../../../schemas/rules-of-engagement.md).
- `assessment_id` (optional) — correlating assessment identifier.

---

## Result

```yaml
endpoints:

relationships:

observations:

evidence:

findings:

status:

metrics:
```

- `endpoints` — canonical `endpoint` [Assets](../../../schemas/asset.md) enriched
  with parameter facts.
- `relationships` —
  [Asset Relationships](../../../schemas/asset-relationship.md).
- `observations` — [Observations](../../../schemas/observation.md) recorded.
- `evidence` — [Evidence](../../../schemas/evidence.md) references.
- `findings` — [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md).
- `status` — one of `completed`, `partial`, `denied`, `error`.
- `metrics` — counters such as endpoints enriched and parameters found.

---

# Behavioral Contract

The skill SHALL

- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  action and proceed only on `allow`
- Honor the attached rate ceiling
- Extract endpoints and parameters through the shared Browser and HTTP Client
- Produce only canonical domain objects
- Record Observations and promote Evidence
- Emit Findings only with supporting Evidence
- Return `denied` when policy denies the required actions

The skill SHALL NOT

- Perform HTTP or browser input or output directly
- Test parameters for vulnerabilities
- Act on out-of-scope applications

---

# Error Semantics

Errors are reported per the [error model](error-model.md). Policy denial yields a
`denied` status. Transport or rendering failures yield `partial` or `error` with
Evidence where available.

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
