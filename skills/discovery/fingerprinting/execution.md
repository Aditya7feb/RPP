# Fingerprinting Execution Model

**File:** `skills/discovery/fingerprinting/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Fingerprinting Skill.

The execution model describes how the skill collects signals for an Asset and
produces canonical Technology records, Observations, Evidence, Findings, and Risk,
gated by the Policy Engine.

The model is deterministic given the same signals.

---

# Execution Overview

```
Receive Asset Target

↓

Resolve Configuration

↓

Consult Policy Engine

↓

Collect Signals (HTTP / TLS Client)

↓

Match Technologies And Grade Confidence

↓

Record Observations → Evidence

↓

Produce Technology Records And Links

↓

Analyze For Weaknesses

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve signal sources, active toggles, matching thresholds, and
analysis toggles using the precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before collecting signals, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the target, the
`fingerprinting` action class, and the intrusiveness implied by the signal
sources.

- `deny` → collection SHALL be skipped and recorded
- `requires_approval` → collection SHALL be routed to approval and deferred
- `allow` → collection SHALL proceed within the attached rate ceiling

Passive signals SHOULD be preferred; active probing SHALL be gated accordingly.
Out-of-scope Assets SHALL never be fingerprinted.

---

# Stage 3 — Signal Collection

The skill SHALL collect signals through the
[HTTP Client](../../shared/http-client/README.md) and
[TLS Client](../../shared/tls-client/README.md).

The skill SHALL NOT perform HTTP or TLS input or output directly.

---

# Stage 4 — Technology Matching

The skill SHALL match collected signals to technologies and versions and SHALL
grade identification confidence, distinguishing observed from inferred
identifications.

Technologies below `min_confidence` SHALL NOT be recorded.

---

# Stage 5 — Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) for the
matched signals and promote corroborated observations to
[Evidence](../../../schemas/evidence.md).

---

# Stage 6 — Technology Production

The skill SHALL produce canonical
[Technology](../../../schemas/technology.md) records and link each to the
fingerprinted [Asset](../../../schemas/asset.md) through an
[Asset Relationship](../../../schemas/asset-relationship.md), deduplicating
equivalent technologies.

---

# Stage 7 — Weakness Analysis

Where enabled, the skill SHALL analyze identified technologies for weaknesses such
as outdated versions and verbose version disclosure.

Where a version is identified, the skill MAY reference known-vulnerability
identifiers informally; deterministic mapping is deferred to a future knowledge
capability.

---

# Stage 8 — Finding And Risk Emission

For each confirmed weakness, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 9 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical signals, the skill SHALL produce identical Technology
identifications, confidence grades, and Findings apart from timestamps and
identifiers.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes collection.
- The [HTTP Client](../../shared/http-client/README.md) and
  [TLS Client](../../shared/tls-client/README.md) provide signals.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- Web Security and API Security skills consume identified Technologies.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failure to collect one signal SHALL NOT abort collection of others; the outcome
SHALL be `partial` where some signals were not collected.

---

# Execution Outputs

The execution model SHALL produce

- Technology records linked to Assets
- Observations and Evidence references
- Findings with Risk where weaknesses are confirmed
- Fingerprinting metrics

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Technology Schema](../../../schemas/technology.md)
- [Execution Model](../../core/execution-model.md)
