# WebSocket API Security Skill Execution

**File:** `skills/api-security/websocket/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the WebSocket API Security
Skill, stage by stage. Given the same API behavior and configuration, execution SHALL
be reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Transport Analysis
Stage 4  Origin Validation Analysis
Stage 5  Handshake Authentication Analysis
Stage 6  Message Authorization Analysis
Stage 7  Error And Close-Frame Disclosure Analysis
Stage 8  Weakness Analysis And Finding Emission
```

---

# Stage 1 — Intake And Scope Validation

The skill SHALL validate that `target` and referenced Assets are within
[Scope](../../../schemas/scope.md). Out-of-scope targets SHALL be rejected before any
action.

---

# Stage 2 — Policy Consultation

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision
permits the action. A `requires_approval` decision SHALL defer the action to an
`awaiting_approval` state. A `deny` decision SHALL suppress the action.

---

# Stage 3 — Transport Analysis

The skill SHALL evaluate, through the
[WebSocket Client](../../shared/websocket-client/README.md), whether the connection
uses secure transport. A connection established over cleartext SHALL be recorded as an
Observation classified CWE-319. General TLS posture is delegated to TLS Analysis.

---

# Stage 4 — Origin Validation Analysis

The skill SHALL perform bounded handshakes presenting controlled foreign Origin values
and observe whether the server accepts them. Acceptance of an unexpected Origin SHALL
be recorded as an Observation classified CWE-346 (Cross-Site WebSocket Hijacking).

---

# Stage 5 — Handshake Authentication Analysis

The skill SHALL attempt a bounded handshake without valid credentials. Acceptance
SHALL be recorded as an Observation classified CWE-306.

---

# Stage 6 — Message Authorization Analysis

Using two controlled identities, the skill SHALL exchange bounded messages that one
identity SHOULD NOT be authorized to send or receive. Missing enforcement SHALL be
recorded as an Observation classified CWE-285. Confirmation SHALL be minimal and SHALL
NOT enumerate other principals' data.

---

# Stage 7 — Error And Close-Frame Disclosure Analysis

The skill SHALL evaluate whether error frames or close-frame reasons disclose
implementation information. Confirmed disclosure SHALL be recorded as an Observation
classified CWE-209.

---

# Stage 8 — Weakness Analysis And Finding Emission

The skill SHALL analyze recorded Observations, promote supporting ones to
[Evidence](../../../schemas/evidence.md), and emit
[Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md). Every
Finding SHALL reference supporting Evidence.

---

# Determinism

Given identical API behavior, Assets, identities, and configuration, the skill SHALL
produce identical Findings. Non-deterministic API behavior SHALL be reflected
faithfully in Evidence.

---

# Idempotence

Assessment SHALL NOT alter server state beyond bounded, controlled exchanges required
for confirmation. Repeated assessment SHALL NOT accumulate side effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
