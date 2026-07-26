# Docker Cloud Security Skill

**File:** `skills/cloud/docker/README.md`

**Version:** 1.0.0

---

# Purpose

The Docker Cloud Security Skill is a Cloud-Security-tier domain skill that evaluates the
security posture of an in-scope container platform within the Robust PenTest Platform
(RPP).

It interprets provider-native container metadata — image manifests, container settings,
daemon configuration, and runtime capabilities — into evidence-backed findings covering
privileged execution, host exposure, insecure defaults, and embedded secrets.

The skill consumes provider-native metadata from the
[Container Client](../../shared/container-client/README.md). It SHALL NOT call the
container engine directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Docker Cloud Security Skill SHALL

- Evaluate container privilege and capability posture
- Evaluate host exposure such as mounted daemon sockets and host namespaces
- Evaluate insecure defaults such as containers running as root
- Evaluate resource-limit enforcement
- Evaluate secret handling in image and container configuration
- Consume `cloud-resource` [Assets](../../../schemas/asset.md) and enrich them
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md)
- Remain tool independent

---

# Non-Goals

The Docker Cloud Security Skill SHALL NOT

- Call the container engine or perform engine I/O directly
- Enumerate engine resources itself beyond the shared client interface
- Execute containers or workloads
- Assess Kubernetes clusters (that is the Kubernetes Cloud Security skill)
- Assess general server-side TLS posture (that is TLS Analysis)
- Test application-layer weaknesses such as injection or XSS (those are Web Security
  skills)
- Invoke command-line tools or parse their output

Engine transport belongs to the shared Container Client; cluster assessment belongs to the
Kubernetes skill; application weaknesses belong to Web Security skills.

The authentication boundary is explicit. Authentication is performed by the shared
clients through the Authentication tier; this skill verifies security posture and
authorization behavior, while the correctness of authentication mechanisms and protocols
is owned by the Authentication tier. This skill SHALL NOT assess authentication-protocol
correctness.

---

# Design Principles

The Docker Cloud Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same observed metadata
- Read-oriented — it interprets observed metadata and does not mutate the platform or
  execute workloads
- Provider-native — it reasons over container resource models
- Tool independent

---

# Architecture

```
Cloud Security Agent

↓

Docker Cloud Security Skill

├── Policy Gate           → Policy Engine
├── Metadata Collector    → Container Client
├── Privilege Analyzer
├── Host-Exposure Analyzer
├── Insecure-Default Analyzer
├── Resource-Limit Analyzer
├── Secret Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill interprets provider-native metadata and SHALL remain unaware of any engine
implementation.

---

# Responsibilities

The Docker Cloud Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Collecting provider-native metadata through the
  [Container Client](../../shared/container-client/README.md)
- Analyzing privilege, host exposure, insecure defaults, resource limits, and secrets
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Platform Target And Scope

↓

Consult Policy Engine (per action)

↓

Collect Provider-Native Metadata (Container Client)

↓

Analyze Privilege, Host Exposure, Defaults, Limits, And Secrets

↓

Record Observations → Evidence

↓

Analyze For Container Security Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced Finding SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

assets:

engine_scope_ref:

credential_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope container platform. `assets` reference `cloud-resource`
[Assets](../../../schemas/asset.md). `engine_scope_ref` references authorized engines,
images, and containers. `credential_ref` references authorized read credentials by
reference only. `scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill MAY produce and enrich `cloud-resource`
[Assets](../../../schemas/asset.md) representing container resources such as images and
containers. It SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the CIS Docker Benchmark and CWE. The references are
informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Privileged container or added dangerous capabilities (CWE-250)
- Host daemon socket or host path mounted into a container (CWE-284)
- Container configured to run as the root user (CWE-250)
- Secrets embedded in image layers or container environment (CWE-312)
- Missing CPU or memory limits enabling resource exhaustion (CWE-770)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md) with
sensitive values redacted.

---

# Policy Enforcement

The Docker Cloud Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing action.
Metadata collection is a read action and SHALL proceed only on an `allow` decision. Where
a decision is `requires_approval`, the skill SHALL defer the action. The skill SHALL NOT
mutate the platform or execute containers. Out-of-scope engines SHALL never be assessed.

---

# Dependencies

The Docker Cloud Security Skill depends on

- [Container Client](../../shared/container-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Docker Cloud Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Cloud Security Agent and cloud workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for container security weaknesses
- Enriched `cloud-resource` Assets
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Docker Cloud Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Interpret observed metadata without mutating the platform or executing containers
- Protect credentials and sensitive values from evidence and logs
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and CIS Benchmark references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `cloud-resource` Assets, an engine scope, and read credentials
- Rely on the skill for container-specific interpretation
- Route cluster, TLS, and application weaknesses to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Call the container engine directly
- Bypass the Policy Engine
- Request platform mutation or container execution
- Assess out-of-scope engines

---

# Documentation Requirements

This skill includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-docker-cloud-security-skill.md

---

# Related Packages

- [Container Client](../../shared/container-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Docker Cloud Security Skill](adr/ADR-001-docker-cloud-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Image provenance and signature evaluation
- Runtime security-profile posture
- Registry inventory posture
- Correlation with Discovery cloud inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Docker Cloud Security Skill produces evidence-backed Findings for container
security weaknesses by interpreting provider-native metadata, acting strictly within scope
and Rules of Engagement through the Policy Engine, without mutating the platform, executing
containers, or invoking tools directly.
