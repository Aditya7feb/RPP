# TLS Analysis Skill

**File:** `skills/discovery/tls-analysis/README.md`

**Version:** 1.0.0

---

# Purpose

The TLS Analysis Skill is a Discovery-tier domain skill that analyzes the
Transport Layer Security (TLS) posture of in-scope services within the Robust
PenTest Platform (RPP).

It inspects negotiated protocols, cipher suites, certificate chains, and
validation outcomes for `service` [Assets](../../../schemas/asset.md), producing
`certificate` Assets, [Observations](../../../schemas/observation.md), and, where
a weakness is identified, [Findings](../../../schemas/finding.md) with associated
[Risk](../../../schemas/risk.md).

Unlike the [TLS Client](../../shared/tls-client/README.md) shared skill, which
negotiates TLS and reports validation outcomes as data, this skill *interprets*
those outcomes to identify TLS weaknesses. It consumes shared infrastructure and
SHALL NOT invoke TLS tools directly.

---

# Goals

The TLS Analysis Skill SHALL

- Analyze negotiated protocols and cipher suites for in-scope services
- Retrieve and evaluate certificate chains and validation outcomes
- Produce canonical `certificate` Assets and relationships
- Emit Observations and Evidence for every analysis
- Identify TLS-related weaknesses as Findings with Risk
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  action
- Remain tool independent

---

# Non-Goals

The TLS Analysis Skill SHALL NOT

- Negotiate TLS directly
- Assign trust verdicts within the transport layer
- Exploit TLS weaknesses
- Act on out-of-scope services
- Invoke TLS command-line tools or parse their output

Negotiation and validation-outcome reporting belong to the
[TLS Client](../../shared/tls-client/README.md); exploitation is out of scope for
Discovery. This skill interprets validation outcomes as weaknesses where
appropriate.

---

# Design Principles

The TLS Analysis Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every produced Asset and Finding
- Deterministic given the same inputs and TLS results
- Confidence-graded
- Interception-aware
- Tool independent

---

# Architecture

```
Recon Agent

↓

TLS Analysis Skill

├── Policy Gate            → Policy Engine
├── Handshake Analyzer      → TLS Client
├── Certificate Evaluator
├── Asset Builder
├── Weakness Analyzer
├── Evidence Recorder      → Evidence
└── Finding Emitter

↓

Assets · Relationships · Observations · Evidence · Findings · Risk
```

The skill orchestrates the TLS Client to interpret TLS posture. It SHALL remain
unaware of any TLS implementation.

---

# Responsibilities

The TLS Analysis Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  action
- Analyzing handshakes and certificates through the
  [TLS Client](../../shared/tls-client/README.md)
- Building `certificate` [Assets](../../../schemas/asset.md) and relationships to
  the analyzed service
- Recording [Observations](../../../schemas/observation.md) and promoting them to
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) and
  [Risk](../../../schemas/risk.md) for TLS weaknesses

---

# Discovery Lifecycle

```
Receive Service Target

↓

Consult Policy Engine (per action)

↓

Analyze Handshake And Certificate (TLS Client)

↓

Record Observations → Evidence

↓

Build Certificate Asset

↓

Analyze For TLS Weaknesses

↓

Emit Findings and Risk (where applicable)
```

Every produced object SHALL be traceable to evidence.

---

# Inputs

The skill accepts

```yaml
target:

service_asset_id:

checks:

scope_id:

roe_id:
```

`target` SHALL be an in-scope TLS service endpoint.

`service_asset_id` MAY reference the `service` Asset being analyzed.

`checks` SHALL declare the analyses to perform, such as `protocols`, `ciphers`,
`certificate`, and `validation`.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill SHALL produce canonical [Assets](../../../schemas/asset.md) of type
`certificate` and
[Asset Relationships](../../../schemas/asset-relationship.md) linking the
certificate to the analyzed `service` Asset via `serves` or `belongs-to`.

Each Asset SHALL carry provenance and a `scope_status` set from the assessment
Scope.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for TLS weaknesses such as

- Deprecated protocol versions offered
- Weak or insecure cipher suites offered
- Expired, self-signed, or hostname-mismatched certificates
- Incomplete or untrusted certificate chains

Interception boundaries reported by the TLS Client SHALL be honored so that a
legitimate intercepting proxy is not reported as a certificate weakness.

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md).

---

# Policy Enforcement

The TLS Analysis Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every action and
SHALL proceed only on an `allow` decision. Out-of-scope services SHALL never be
analyzed.

---

# Dependencies

The TLS Analysis Skill depends on

- [TLS Client](../../shared/tls-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Asset Relationship Schema](../../../schemas/asset-relationship.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The TLS Analysis Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Recon Agent and recon workflows
- Fingerprinting, which correlates TLS facts with technology identification
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Certificate Assets and relationships
- Observations and Evidence references
- Findings with Risk for TLS weaknesses

Outputs SHALL remain implementation independent.

---

# Security Principles

The TLS Analysis Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Honor interception boundaries to avoid spurious findings
- Produce no Finding without supporting Evidence
- Report weaknesses as data; exploitation is out of scope
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope TLS service and the related service Asset
- Rely on the skill for certificate Asset construction
- Correlate produced certificate Assets with Fingerprinting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Negotiate TLS directly
- Bypass the Policy Engine
- Report interception boundaries as certificate weaknesses
- Act on out-of-scope services

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
- adr/ADR-001-tls-analysis-skill.md

---

# Related Packages

- [TLS Client](../../shared/tls-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Asset Relationship](../../../schemas/asset-relationship.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — TLS Analysis Skill](adr/ADR-001-tls-analysis-skill.md)

---

# Future Extensions

Future versions MAY support

- Certificate transparency correlation
- Post-quantum negotiation observation
- OCSP and revocation-state reporting
- Cipher-preference-order analysis

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant TLS Analysis Skill produces a canonical, evidence-backed view of TLS
posture — certificate Assets and TLS-weakness Findings — while honoring
interception boundaries and acting strictly within scope and Rules of Engagement
through the Policy Engine, without invoking TLS tools directly.
