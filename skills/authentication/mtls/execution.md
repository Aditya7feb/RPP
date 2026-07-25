# Mutual TLS Authentication Execution Model

**File:** `skills/authentication/mtls/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Mutual TLS
Authentication Skill, stage by stage. Given the same inputs, configuration, and
service behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Observe Client-Certificate Handshake (TLS Client)

↓

Observe Application Behavior (HTTP Client)

↓

Analyze Validation, Revocation, And Fallback

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
before every target-facing action. Handshake and application probing are `active`
actions. Only an `allow` decision permits the action, and the attached rate ceiling
SHALL be honored. A `requires_approval` decision SHALL defer the action until
approval is granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Observe Client-Certificate Handshake

The skill SHALL observe whether a client certificate is required and how presented
certificate variants are handled through the
[TLS Client](../../shared/tls-client/README.md), capturing the canonical
[TLS Connection](../../../schemas/tls-connection.md) and
[TLS Validation Result](../../../schemas/tls-validation-result.md). The skill SHALL
NOT open connections directly.

---

# Stage 4 — Observe Application Behavior

The skill SHALL observe application behavior with and without a client certificate
through the [HTTP Client](../../shared/http-client/README.md) to detect fallback to
weaker authentication.

---

# Stage 5 — Analyze Validation, Revocation, And Fallback

The skill SHALL analyze certificate and chain validation, identity binding,
revocation checking, and fallback behavior using deterministic criteria and the
canonical validation result.

---

# Stage 6 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Private key material SHALL be redacted.

---

# Stage 7 — Analyze For Weaknesses

The skill SHALL analyze the observations for mutual TLS weaknesses using
deterministic criteria. Analysis SHALL be separate from observation.

---

# Stage 8 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 9 — Return Result

The skill SHALL return findings, observations, evidence, a `status`, and metrics
per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from observation.
- Validation outcomes are interpreted from the canonical validation result.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial results SHALL
be returned with Evidence where available. Policy denial SHALL always fail closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [TLS Client Execution](../../shared/tls-client/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
