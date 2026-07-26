# XML External Entity Skill

**File:** `skills/web-security/xxe/README.md`

**Version:** 1.0.0

---

# Purpose

The XML External Entity Skill is a Web-Security-tier domain skill that evaluates
whether an in-scope web application unsafely processes XML external entities within
the Robust PenTest Platform (RPP).

It examines whether an XML parser resolves external entities from user-controllable
input, reporting weaknesses confirmed through bounded, non-sensitive entity resolution
and out-of-band interaction signals (CWE-611).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The XML External Entity Skill SHALL

- Evaluate XML-processing endpoints for unsafe external-entity resolution
- Confirm resolution using bounded, non-sensitive entities and out-of-band signals
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for XXE weaknesses
- Remain tool independent

---

# Non-Goals

The XML External Entity Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test server-side request forgery in general (that is the SSRF skill)
- Read, exfiltrate, or modify sensitive files
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; general request-forgery testing belongs to the SSRF skill; reading sensitive
files is prohibited.

---

# Design Principles

The XML External Entity Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms resolution without reading sensitive files
- Non-destructive — its entities reference only bounded, non-sensitive or controlled
  resources
- Tool independent

---

# Architecture

```
Web Security Agent

↓

XML External Entity Skill

├── Policy Gate            → Policy Engine
├── Entity Prober         → HTTP Client
├── Resolution Analyzer
├── Out-Of-Band Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe entity-resolution behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The XML External Entity Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Submitting bounded entity probes and observing responses through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing in-band resolution and out-of-band interaction signals
- Confirming external-entity resolution without reading sensitive files
- Recording [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Emitting [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md)

---

# Assessment Lifecycle

```
Receive Target And Assets

↓

Consult Policy Engine (per action)

↓

Submit Bounded Entity Probes (HTTP Client)

↓

Observe In-Band And Out-Of-Band Resolution

↓

Record Observations → Evidence

↓

Analyze For XXE Weaknesses

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

marker_ref:

collector_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL that processes XML.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test.

`marker_ref` MAY reference a non-sensitive resource used to confirm entity resolution.

`collector_ref` MAY reference a controlled out-of-band collector used to confirm
interaction.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. It SHALL NOT invent Asset types.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- XML external entity resolution confirmed by a bounded, non-sensitive entity
  (CWE-611)
- Out-of-band entity resolution confirmed via a controlled collector
- XML parsing configured to resolve external entities or document type definitions
  unsafely

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only non-sensitive resolution recorded and sensitive content redacted.

---

# Policy Enforcement

The XML External Entity Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Entity probing is an `active`, high-impact action; it SHALL proceed only on
an `allow` decision and within the attached rate ceiling, and SHALL commonly require
approval under the Rules of Engagement. Where a decision is `requires_approval`, the
skill SHALL defer the action until approval is granted. The skill SHALL confirm
resolution using non-sensitive or controlled resources and SHALL NOT read sensitive
files. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The XML External Entity Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The XML External Entity Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- API Security skills that process XML payloads
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for XXE weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The XML External Entity Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm resolution using non-sensitive or controlled resources only
- Never read, exfiltrate, or modify sensitive files
- Reference managed markers and authorized collectors only
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-611
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope XML-processing `endpoint` and `api` Assets
- Provide a non-sensitive marker and a controlled collector where permitted
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Reference sensitive files in entity probes
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
- adr/ADR-001-xxe-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Path Traversal](../path-traversal/README.md)
- SSRF (Web Security tier, planned)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — XML External Entity Skill](adr/ADR-001-xxe-skill.md)

---

# Future Extensions

Future versions MAY support

- Parameter-entity and blind-XXE confirmation via richer out-of-band channels
- Document-type-definition configuration analysis
- Correlation of XXE with SSRF and file-disclosure exploitability
- Billion-laughs and entity-expansion exposure assessment under stricter approval

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant XML External Entity Skill produces evidence-backed Findings for XXE
weaknesses while acting strictly within scope and Rules of Engagement through the
Policy Engine, confirming resolution with non-sensitive or controlled resources, and
never reading sensitive files or invoking tools directly.
