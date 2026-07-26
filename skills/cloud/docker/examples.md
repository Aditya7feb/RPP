# Docker Cloud Security Skill Examples

**File:** `skills/cloud/docker/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-free examples of the Docker Cloud Security
Skill. Examples illustrate the interface and outputs; they contain no implementation code.

---

# Example 1 — Privileged Container

## Request

```yaml
target: container-platform-prod
assets:
  - asset-cloud-6401
engine_scope_ref: docker-scope-example
credential_ref: docker-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_privilege: true
```

## Result

```yaml
findings:
  - id: finding-docker-5001
    title: Container runs in privileged mode
    weakness: CWE-250
    benchmark: CIS Docker - do not use privileged containers
    asset: asset-cloud-6401
    risk_ref: risk-docker-3001
    evidence_refs:
      - evidence-docker-7001
observations:
  - id: obs-docker-4001
    kind: privilege-analysis
evidence:
  - id: evidence-docker-7001
    observation_ref: obs-docker-4001
status: completed
metrics:
  resources_evaluated: 20
  findings: 1
```

The Container Client reports the container's privileged flag; the skill interprets it as a
privilege weakness.

---

# Example 2 — Host Daemon Socket Mounted

## Request

```yaml
target: container-platform-prod
assets:
  - asset-cloud-6402
engine_scope_ref: docker-scope-example
credential_ref: docker-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_host_exposure: true
```

## Result

```yaml
findings:
  - id: finding-docker-5002
    title: Container mounts the host engine socket
    weakness: CWE-284
    benchmark: CIS Docker - do not mount the daemon socket
    asset: asset-cloud-6402
    risk_ref: risk-docker-3002
    evidence_refs:
      - evidence-docker-7002
status: completed
metrics:
  resources_evaluated: 20
  findings: 1
```

The Container Client reports the mount configuration; the skill interprets the mounted host
socket as host exposure.

---

# Example 3 — Secret Embedded In Image

## Request

```yaml
target: container-platform-prod
assets:
  - asset-cloud-6403
engine_scope_ref: docker-scope-example
credential_ref: docker-read-credential
scope_id: scope-example-2024
roe_id: roe-example-2024
options:
  check_secrets: true
```

## Result

```yaml
findings:
  - id: finding-docker-5003
    title: Image environment embeds a credential
    weakness: CWE-312
    benchmark: CIS Docker - do not store secrets in images
    asset: asset-cloud-6403
    risk_ref: risk-docker-3003
    evidence_refs:
      - evidence-docker-7003
status: completed
metrics:
  resources_evaluated: 20
  findings: 1
```

The Container Client reports the image environment; the skill interprets the embedded
credential as a secret exposure. The credential value is redacted in evidence.

---

# Example 4 — Requires Approval

## Request

```yaml
target: container-platform-prod
engine_scope_ref: docker-scope-example
scope_id: scope-example-2024
roe_id: roe-example-2024
```

## Result

```yaml
findings: []
status: awaiting_approval
metrics:
  approvals_requested: 1
```

The Rules of Engagement require approval before metadata collection; the skill defers until
approval is granted.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [configuration.md](configuration.md)
- [error-model.md](error-model.md)
