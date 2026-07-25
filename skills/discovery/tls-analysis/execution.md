# TLS Analysis Execution Model

**File:** `skills/discovery/tls-analysis/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the TLS Analysis Skill.

The execution model describes how the skill analyzes TLS posture for a service and
produces canonical Assets, Observations, Evidence, Findings, and Risk, gated by
the Policy Engine.

The model is deterministic given the same inputs and TLS results.

---

# Execution Overview

```
Receive Service Target

↓

Resolve Configuration

↓

Consult Policy Engine

↓

Analyze Handshake And Certificate (TLS Client)

↓

Record Observations → Evidence

↓

Build Certificate Asset

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

The skill SHALL resolve checks, thresholds, and interception handling using the
precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before analysis, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the target, the
`fingerprinting` action class, and `active` intrusiveness.

- `deny` → analysis SHALL be skipped and recorded
- `requires_approval` → analysis SHALL be routed to approval and deferred
- `allow` → analysis SHALL proceed within the attached rate ceiling

Out-of-scope services SHALL never be analyzed.

---

# Stage 3 — Handshake And Certificate Analysis

The skill SHALL analyze protocols, ciphers, and certificate chains through the
[TLS Client](../../shared/tls-client/README.md).

The skill SHALL NOT negotiate TLS directly.

Validation outcomes SHALL be received from the TLS Client as data; interception
boundaries SHALL be honored.

---

# Stage 4 — Observation And Evidence

The skill SHALL record [Observations](../../../schemas/observation.md) for
negotiated parameters and certificate facts and promote corroborated observations
to [Evidence](../../../schemas/evidence.md).

---

# Stage 5 — Certificate Asset Construction

The skill SHALL build a canonical `certificate`
[Asset](../../../schemas/asset.md) and an
[Asset Relationship](../../../schemas/asset-relationship.md) linking it to the
analyzed `service` Asset, deduplicating by `canonical_key`.

---

# Stage 6 — Weakness Analysis

The skill SHALL analyze results against thresholds for weaknesses such as
deprecated protocols, weak ciphers, and invalid certificates.

A validation outcome caused by a legitimate interception boundary SHALL NOT be
flagged as a certificate weakness.

---

# Stage 7 — Finding And Risk Emission

For each confirmed weakness, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 8 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical inputs and TLS results, the skill SHALL produce identical Assets
and Findings apart from timestamps and identifiers.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes analysis.
- The [TLS Client](../../shared/tls-client/README.md) performs negotiation and
  reports validation outcomes and interception boundaries.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- Fingerprinting correlates certificate facts with technology identification.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A failure for one check SHALL NOT abort other checks; the outcome SHALL be
`partial` where some checks did not complete.

---

# Execution Outputs

The execution model SHALL produce

- A certificate Asset and relationship
- A TLS summary reported as data
- Findings with Risk where weaknesses are confirmed
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [TLS Client](../../shared/tls-client/README.md)
- [Execution Model](../../core/execution-model.md)
