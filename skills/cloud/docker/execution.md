# Docker Cloud Security Skill Execution

**File:** `skills/cloud/docker/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Docker Cloud Security Skill,
stage by stage. Given the same observed metadata and configuration, execution SHALL be
reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Metadata Collection
Stage 4  Privilege Analysis
Stage 5  Host-Exposure Analysis
Stage 6  Insecure-Default And Resource-Limit Analysis
Stage 7  Secret Analysis
Stage 8  Weakness Analysis And Finding Emission
```

---

# Stage 1 — Intake And Scope Validation

The skill SHALL validate that the target and referenced Assets are within
[Scope](../../../schemas/scope.md). Out-of-scope engines SHALL be rejected before any
action.

---

# Stage 2 — Policy Consultation

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
action. A `requires_approval` decision SHALL defer the action.

---

# Stage 3 — Metadata Collection

The skill SHALL collect provider-native metadata through the
[Container Client](../../shared/container-client/README.md) using inspect, list, and get
operations. Collection is read-only and bounded by configured limits.

---

# Stage 4 — Privilege Analysis

The skill SHALL interpret privilege and capability configuration and record privileged
containers or dangerous capabilities as Observations classified CWE-250.

---

# Stage 5 — Host-Exposure Analysis

The skill SHALL interpret mount and namespace configuration and record host socket or path
mounts and host namespace sharing as Observations classified CWE-284.

---

# Stage 6 — Insecure-Default And Resource-Limit Analysis

The skill SHALL interpret user and resource configuration and record root execution as
Observations classified CWE-250 and missing resource limits as Observations classified
CWE-770.

---

# Stage 7 — Secret Analysis

The skill SHALL interpret image and container configuration and record embedded secrets as
Observations classified CWE-312.

---

# Stage 8 — Weakness Analysis And Finding Emission

The skill SHALL analyze recorded Observations, promote supporting ones to
[Evidence](../../../schemas/evidence.md), and emit
[Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md). Every
Finding SHALL reference supporting Evidence.

---

# Determinism

Given identical observed metadata, Assets, and configuration, the skill SHALL produce
identical Findings.

---

# Idempotence

Assessment SHALL NOT alter the platform or execute containers. Repeated assessment SHALL NOT
accumulate side effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
