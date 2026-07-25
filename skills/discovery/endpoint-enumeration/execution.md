# Endpoint Enumeration Execution Model

**File:** `skills/discovery/endpoint-enumeration/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Endpoint
Enumeration Skill, stage by stage. Given the same inputs, configuration, and
application behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Render And Retrieve (Browser / HTTP Client)

↓

Extract Endpoints And Parameters

↓

Mine Parameters (bounded, optional)

↓

Record Observations → Evidence

↓

Build Endpoint Assets

↓

Analyze Weaknesses

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
before every action. Rendering, script retrieval, and parameter mining are
`active` actions. Only an `allow` decision permits the action, and the attached
rate ceiling SHALL be honored. A denial for the primary target SHALL yield a
`denied` status with no enumeration.

---

# Stage 3 — Render And Retrieve

For authorized actions the skill SHALL render pages through the
[Browser](../../shared/browser/README.md) and retrieve scripts through the
[HTTP Client](../../shared/http-client/README.md). The skill SHALL NOT perform
rendering or requests directly.

---

# Stage 4 — Extract Endpoints And Parameters

The skill SHALL extract endpoints and parameters from rendered content and
scripts, including forms, links, fetch and XHR targets, and inline handlers where
configured.

---

# Stage 5 — Mine Parameters

When parameter mining is enabled the skill SHALL mine additional parameters within
the configured bounds and the policy rate ceiling. Mined parameters SHALL be
graded at lower confidence than observed parameters.

---

# Stage 6 — Record Observations And Evidence

Every extraction and mining action SHALL yield an
[Observation](../../../schemas/observation.md) promoted to
[Evidence](../../../schemas/evidence.md). Client-side secrets SHALL be redacted per
Rules of Engagement.

---

# Stage 7 — Build Endpoint Assets

The skill SHALL construct or enrich canonical `endpoint`
[Assets](../../../schemas/asset.md) with parameter facts, attach provenance, set
`scope_status` from Scope, and produce `references`
[Asset Relationships](../../../schemas/asset-relationship.md).

---

# Stage 8 — Analyze Weaknesses

The skill SHALL analyze enriched endpoints for hidden-parameter and
undocumented-endpoint exposure using deterministic criteria. Analysis SHALL be
separate from extraction.

---

# Stage 9 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 10 — Return Result

The skill SHALL return endpoints, relationships, observations, evidence, findings,
a `status`, and metrics per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Assets and Findings.
- Analysis is separated from extraction.
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
- [Browser Execution](../../shared/browser/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
