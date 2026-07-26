# Kubernetes Cloud Security Skill Configuration

**File:** `skills/cloud/kubernetes/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Kubernetes Cloud Security Skill
and the precedence rules that govern it. Configuration describes structure and intent only.

---

# Configuration Object

```yaml
kubernetes_cloud_security:
  checks:
    rbac: true
    workloads: true
    exposure: true
    network_policy: true
    secrets: true

  limits:
    max_resources:

  evidence:
    redact_sensitive: true
```

---

# Field Definitions

## checks

Each boolean under `checks` enables or disables a capability. All checks default to `true`.

## limits

`max_resources` bounds the number of resources interpreted per assessment. The skill SHALL
NOT exceed this bound.

## evidence

`redact_sensitive` SHALL default to `true`, requiring redaction of sensitive values such
as secret contents.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-assessment `options` in the `assess` request
4. Skill configuration in this document
5. Documented defaults

Rules of Engagement and Policy Engine decisions SHALL always override requested options.

---

# Validation Rules

- `max_resources` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
