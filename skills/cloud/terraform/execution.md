# Terraform Cloud Security Skill Execution

**File:** `skills/cloud/terraform/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Terraform Cloud Security
Skill, stage by stage. Given the same configuration files, execution SHALL be reproducible.

---

# Execution Stages

```
Stage 1  Intake And Scope Validation
Stage 2  Policy Consultation
Stage 3  Configuration Reading
Stage 4  Resource Configuration Analysis
Stage 5  Exposure And Encryption Analysis
Stage 6  Access And Secret Analysis
Stage 7  Weakness Analysis And Finding Emission
```

---

# Stage 1 — Intake And Scope Validation

The skill SHALL validate that the target and configuration root are within
[Scope](../../../schemas/scope.md). Out-of-scope configuration roots SHALL be rejected
before any action.

---

# Stage 2 — Policy Consultation

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md). Only an `allow` decision permits the
action. A `requires_approval` decision SHALL defer the action.

---

# Stage 3 — Configuration Reading

The skill SHALL read declared configuration through the
[Filesystem Client](../../shared/filesystem-client/README.md) within the authorized root.
Reading is bounded by configured file and resource limits. No infrastructure is provisioned
or contacted.

---

# Stage 4 — Resource Configuration Analysis

The skill SHALL interpret declared resource configuration and record insecure settings such
as missing logging as Observations classified CWE-778 or CWE-1188.

---

# Stage 5 — Exposure And Encryption Analysis

The skill SHALL interpret declared configuration and record public exposure as Observations
classified CWE-284 and missing encryption at rest as Observations classified CWE-311.

---

# Stage 6 — Access And Secret Analysis

The skill SHALL interpret declared access grants and configuration and record
over-permissive grants as Observations classified CWE-732 and hardcoded secrets as
Observations classified CWE-798.

---

# Stage 7 — Weakness Analysis And Finding Emission

The skill SHALL analyze recorded Observations, promote supporting ones to
[Evidence](../../../schemas/evidence.md), and emit
[Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md). Every
Finding SHALL reference supporting Evidence.

---

# Determinism

Given identical configuration files and settings, the skill SHALL produce identical
Findings.

---

# Idempotence

Assessment SHALL NOT provision, plan, or apply infrastructure. Repeated assessment SHALL NOT
accumulate side effects.

---

# Related Documents

- [interface.md](interface.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
- [examples.md](examples.md)
