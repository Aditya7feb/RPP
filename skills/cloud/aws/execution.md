# AWS Cloud Security Skill Execution

**File:** `skills/cloud/aws/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the AWS Cloud Security Skill,
stage by stage. Given the same observed metadata and configuration, execution SHALL be
reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Metadata Collection
Stage 4  IAM Posture Analysis
Stage 5  Exposure Analysis
Stage 6  Encryption Analysis
Stage 7  Insecure-Default Analysis
Stage 8  Weakness Analysis And Finding Emission
```

---

# Stage 1 — Intake And Scope Validation

The skill SHALL validate that the target and referenced Assets are within
[Scope](../../../schemas/scope.md). Out-of-scope accounts SHALL be rejected before any
action.

---

# Stage 2 — Policy Consultation

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits
the action. A `requires_approval` decision SHALL defer the action.

---

# Stage 3 — Metadata Collection

The skill SHALL collect provider-native metadata through the
[AWS Client](../../shared/aws-client/README.md) and storage exposure metadata through the
[Cloud Storage Client](../../shared/cloud-storage-client/README.md). Collection is
read-only and bounded by configured limits.

---

# Stage 4 — IAM Posture Analysis

The skill SHALL interpret IAM principals, policies, and effective permissions and record
over-permissive grants as Observations classified CWE-732 or CWE-269.

---

# Stage 5 — Exposure Analysis

The skill SHALL interpret storage access, resource sharing, and network metadata and
record public or unrestricted exposure as Observations classified CWE-284.

---

# Stage 6 — Encryption Analysis

The skill SHALL interpret storage, volume, and database configuration and record missing
encryption at rest as Observations classified CWE-311.

---

# Stage 7 — Insecure-Default Analysis

The skill SHALL interpret instance metadata service configuration and other defaults and
record insecure settings, such as permitting IMDSv1, as Observations classified CWE-1188.

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

Assessment SHALL NOT alter the environment. Repeated assessment SHALL NOT accumulate side
effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
