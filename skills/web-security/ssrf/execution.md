# Server-Side Request Forgery Execution Model

**File:** `skills/web-security/ssrf/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Server-Side Request
Forgery Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Submit Bounded Probes Toward Controlled Destination (HTTP Client)

↓

Observe Out-Of-Band And Differential Signals

↓

Record Observations → Evidence

↓

Analyze For SSRF Weaknesses

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
before every target-facing action. Forgery probing is an `active`, high-impact action.
Only an `allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Submit Bounded Probes Toward Controlled Destination

For authorized request-issuing parameters the skill SHALL submit bounded probes that
reference a controlled destination or collector through the
[HTTP Client](../../shared/http-client/README.md). The skill SHALL NOT target
internal services, cloud metadata, or sensitive endpoints, and SHALL NOT perform
requests directly.

---

# Stage 4 — Observe Out-Of-Band And Differential Signals

The skill SHALL observe whether an out-of-band interaction reaches the controlled
collector and whether response or timing differentials indicate a server-side fetch,
capturing the canonical [HTTP Timing](../../../schemas/http-timing.md) representation.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Only the controlled-destination
interaction SHALL be recorded, and any incidental sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For SSRF Weaknesses

The skill SHALL analyze the observations for server-side request forgery using
deterministic criteria and classify them using canonical weakness identifiers such as
CWE-918. Analysis SHALL be separate from observation.

---

# Stage 7 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 8 — Return Result

The skill SHALL return findings, observations, evidence, a `status`, and metrics
per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from probing and observation.
- Confirmation targets only a controlled destination.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial results SHALL
be returned with Evidence where available. Policy denial SHALL always fail closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Client Execution](../../shared/http-client/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
