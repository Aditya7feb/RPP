# gRPC API Security Skill

**File:** `skills/api-security/grpc/README.md`

**Version:** 1.0.0

---

# Purpose

The gRPC API Security Skill is an API-Security-tier domain skill that evaluates the
security of an in-scope gRPC API within the Robust PenTest Platform (RPP).

It focuses on gRPC-specific weaknesses — server reflection exposure, transport
security, method- and object-level authorization, and message-size and streaming
resource consumption — reporting weaknesses confirmed through bounded, non-destructive
verification aligned to the OWASP API Security Top 10 (2023).

The skill consumes the `api`, `endpoint`, and `service`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[gRPC Client](../../shared/grpc-client/README.md) and SHALL NOT open connections
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The gRPC API Security Skill SHALL

- Evaluate server reflection exposure and method disclosure
- Evaluate transport security for gRPC channels
- Evaluate method- and object-level authorization across identities
- Evaluate message-size and streaming resource-consumption controls
- Consume `api`, `endpoint`, and `service` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for gRPC security weaknesses
- Remain tool independent

---

# Non-Goals

The gRPC API Security Skill SHALL NOT

- Open gRPC connections or perform message input or output directly
- Discover services or methods (that is Discovery)
- Analyze general server-side TLS posture (that is TLS Analysis)
- Test generic injection such as SQL or command injection (those are Web Security
  skills)
- Enumerate or exfiltrate other principals' data beyond minimal confirmation
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared gRPC Client; discovery belongs to the Discovery
tier; general TLS posture belongs to TLS Analysis; generic injection belongs to Web
Security skills.

---

# Design Principles

The gRPC API Security Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same API behavior
- Conservative — it confirms authorization and consumption gaps with bounded probes
- Privacy-preserving — it uses only authorized controlled identities
- Tool independent

---

# Architecture

```
API Security Agent

↓

gRPC API Security Skill

├── Policy Gate            → Policy Engine
├── Method Prober         → gRPC Client
├── Reflection Analyzer
├── Transport Analyzer
├── Method Authorization Analyzer
├── Resource Consumption Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the gRPC Client to observe gRPC behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The gRPC API Security Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Invoking bounded gRPC methods across two controlled identities through the
  [gRPC Client](../../shared/grpc-client/README.md)
- Analyzing reflection exposure, transport security, method authorization, and
  resource consumption
- Confirming gaps with minimal, controlled invocations
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive API Target And Assets

↓

Consult Policy Engine (per action)

↓

Invoke Bounded Methods Across Controlled Identities (gRPC Client)

↓

Analyze Reflection, Transport, Authorization, And Consumption

↓

Record Observations → Evidence

↓

Analyze For gRPC Security Weaknesses

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

identities_ref:

descriptor_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope gRPC service endpoint.

`assets` reference the `api`, `endpoint`, and `service`
[Assets](../../../schemas/asset.md) under test.

`identities_ref` MAY reference two authorized, controlled test identities. It SHALL be
a reference, never inline credentials.

`descriptor_ref` MAY reference a discovered service descriptor that enumerates methods
and messages.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It MAY enrich the `api`
[Asset](../../../schemas/asset.md) with method facts and SHALL NOT invent Asset types.

---

# Produced Findings

These weaknesses align with the OWASP API Security Top 10 (2023), primarily API5
(BFLA), API1 (BOLA), API4 (Unrestricted Resource Consumption), and API8 (Security
Misconfiguration), and with the OWASP Top 10 (2021) categories A05:2021 – Security
Misconfiguration and A01:2021 – Broken Access Control. These references are
informational and do not change capability scope.

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Server reflection enabled in production, disclosing service and method detail
  (CWE-200)
- gRPC channel established without transport encryption (CWE-319)
- Method- or object-level authorization not enforced across identities (CWE-285)
- Missing message-size or streaming limits enabling resource exhaustion (CWE-770)
- Verbose status detail disclosing implementation information (CWE-209)

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only minimal controlled confirmation recorded and sensitive content redacted.

---

# Policy Enforcement

The gRPC API Security Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Method invocation is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Message-size and streaming probes SHALL be bounded to avoid denial of service, and
the skill SHALL use only authorized controlled identities. Out-of-scope targets SHALL
never be tested.

---

# Dependencies

The gRPC API Security Skill depends on

- [gRPC Client](../../shared/grpc-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The gRPC API Security Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The API Security Agent and API-security workflows
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for gRPC security weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The gRPC API Security Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound message-size and streaming probes to avoid denial of service
- Use only authorized controlled identities for authorization testing
- Confirm authorization gaps with minimal, controlled invocations only
- Never enumerate or exfiltrate other principals' data
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical identifiers and OWASP API Security references
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `api` and `service` Assets, a discovered descriptor, and two
  controlled identities
- Rely on the skill for gRPC-specific evaluation
- Route general TLS posture and generic injection testing to the dedicated skills
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Open gRPC connections directly
- Bypass the Policy Engine
- Send unbounded messages or streams
- Test out-of-scope targets

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
- adr/ADR-001-grpc-api-security-skill.md

---

# Related Packages

- [gRPC Client](../../shared/grpc-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [API Discovery](../../discovery/api-discovery/README.md)
- [TLS Analysis](../../discovery/tls-analysis/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — gRPC API Security Skill](adr/ADR-001-grpc-api-security-skill.md)

---

# Future Extensions

Future versions MAY support

- Protocol-descriptor-driven method modeling
- Streaming-specific abuse evaluation
- Metadata and interceptor authorization evaluation
- Correlation with Discovery API inventory

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant gRPC API Security Skill produces evidence-backed Findings for
gRPC-specific weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, bounding resource-consumption probes, using only controlled
identities, and never denying service or invoking tools directly.
