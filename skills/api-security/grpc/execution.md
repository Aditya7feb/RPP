# gRPC API Security Skill Execution

**File:** `skills/api-security/grpc/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the gRPC API Security
Skill, stage by stage. Given the same API behavior and configuration, execution SHALL
be reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Reflection Analysis
Stage 4  Transport Analysis
Stage 5  Method Authorization Analysis
Stage 6  Object-Level Authorization Analysis
Stage 7  Resource-Consumption Analysis
Stage 8  Status-Detail Disclosure Analysis
Stage 9  Weakness Analysis And Finding Emission
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

# Stage 3 — Reflection Analysis

The skill SHALL evaluate, through the
[gRPC Client](../../shared/grpc-client/README.md), whether server reflection is
enabled and discloses service and method detail. Confirmed production exposure SHALL
be recorded as an Observation classified CWE-200.

---

# Stage 4 — Transport Analysis

The skill SHALL evaluate whether the gRPC channel enforces transport encryption. A
channel accepting cleartext transport SHALL be recorded as an Observation classified
CWE-319. General TLS posture is delegated to TLS Analysis.

---

# Stage 5 — Method Authorization Analysis

Using two controlled identities, the skill SHALL invoke bounded methods that one
identity SHOULD NOT be authorized to call. Successful invocation without enforcement
SHALL be recorded as an Observation classified CWE-285 (OWASP API5:2023).

---

# Stage 6 — Object-Level Authorization Analysis

The skill SHALL request minimally identified objects owned by one identity while
authenticated as another. Successful access SHALL be recorded as an Observation
classified CWE-285 (OWASP API1:2023). Confirmation SHALL be minimal and SHALL NOT
enumerate other principals' data.

---

# Stage 7 — Resource-Consumption Analysis

The skill SHALL send bounded, incrementally larger messages or streams within the
configured ceilings to evaluate size and streaming limits. Absent limits SHALL be
recorded as an Observation classified CWE-770 (OWASP API4:2023). Probes SHALL NOT be
unbounded and SHALL never cause denial of service.

---

# Stage 8 — Status-Detail Disclosure Analysis

The skill SHALL evaluate whether gRPC status detail discloses implementation
information. Confirmed disclosure SHALL be recorded as an Observation classified
CWE-209.

---

# Stage 9 — Weakness Analysis And Finding Emission

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

Assessment SHALL NOT alter server state beyond bounded, controlled invocations
required for confirmation. Repeated assessment SHALL NOT accumulate side effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
