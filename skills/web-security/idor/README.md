# Insecure Direct Object Reference Skill

**File:** `skills/web-security/idor/README.md`

**Version:** 1.0.0

---

# Purpose

The Insecure Direct Object Reference Skill is a Web-Security-tier domain skill that
evaluates whether an in-scope web application exposes objects by reference without
enforcing per-object authorization within the Robust PenTest Platform (RPP).

It examines whether changing an object identifier grants access to another principal's
resource, reporting weaknesses where object references are not authorized against the
requesting identity (CWE-639).

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The Insecure Direct Object Reference Skill SHALL

- Evaluate object-reference parameters for missing per-object authorization
- Confirm unauthorized access using two authorized, controlled test identities
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for IDOR weaknesses
- Remain tool independent

---

# Non-Goals

The Insecure Direct Object Reference Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Test authentication mechanisms (that is the Authentication tier)
- Enumerate or exfiltrate other principals' sensitive data beyond minimal
  confirmation
- Perform destructive or disruptive exploitation
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; authentication testing belongs to the Authentication tier; mass enumeration of
others' data is prohibited.

---

# Design Principles

The Insecure Direct Object Reference Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same application behavior
- Conservative — it confirms unauthorized access with minimal, controlled reads
- Privacy-preserving — it uses only authorized controlled identities and their own
  resources as references
- Tool independent

---

# Architecture

```
Web Security Agent

↓

Insecure Direct Object Reference Skill

├── Policy Gate            → Policy Engine
├── Reference Prober      → HTTP Client
├── Authorization Analyzer
├── Cross-Identity Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe authorization behavior. It SHALL
remain unaware of any transport implementation.

---

# Responsibilities

The Insecure Direct Object Reference Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Requesting object references across two controlled identities through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing whether per-object authorization is enforced
- Confirming unauthorized access with minimal, controlled reads
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

Request Object References Across Controlled Identities (HTTP Client)

↓

Analyze Per-Object Authorization

↓

Record Observations → Evidence

↓

Analyze For IDOR Weaknesses

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

scope_id:

roe_id:
```

`target` SHALL be an in-scope web application or API base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test, including object-reference parameters.

`identities_ref` MAY reference two authorized, controlled test identities and their
own object references. It SHALL be a reference, never inline credentials.

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

- An object reference accessible by an identity that does not own it (CWE-639)
- Missing per-object authorization on read or modify operations
- Predictable identifiers combined with absent authorization
- Horizontal or vertical access-control gaps on referenced objects

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with only minimal controlled confirmation recorded and sensitive content redacted.

---

# Policy Enforcement

The Insecure Direct Object Reference Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Cross-identity probing is an `active` action; it SHALL proceed only on an
`allow` decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted. The
skill SHALL use only authorized controlled identities and SHALL NOT enumerate or
exfiltrate other principals' data. Out-of-scope targets SHALL never be tested.

---

# Dependencies

The Insecure Direct Object Reference Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The Insecure Direct Object Reference Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Web Security Agent and web-security workflows
- API Security skills that assess object-level authorization
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for IDOR weaknesses
- Observations and Evidence references

Outputs SHALL remain implementation independent.

---

# Security Principles

The Insecure Direct Object Reference Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Use only authorized controlled identities and their own references
- Confirm unauthorized access with minimal, controlled reads only
- Never enumerate or exfiltrate other principals' data
- Reference managed identities, never inline credentials
- Produce no Finding without supporting Evidence
- Classify weaknesses using canonical weakness identifiers such as CWE-639
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` and `api` Assets and object-reference parameters
- Provide two authorized controlled test identities
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Enumerate or exfiltrate other principals' data
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
- adr/ADR-001-idor-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Session Management](../../authentication/sessions/README.md)
- File Upload (Web Security tier, planned)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — Insecure Direct Object Reference Skill](adr/ADR-001-idor-skill.md)

---

# Future Extensions

Future versions MAY support

- Vertical privilege-escalation object-access modeling
- Object-identifier-pattern classification
- Correlation with authentication and session context
- Object-level authorization evaluation handoff to API Security

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Insecure Direct Object Reference Skill produces evidence-backed Findings
for IDOR weaknesses while acting strictly within scope and Rules of Engagement through
the Policy Engine, using only authorized controlled identities, confirming with
minimal reads, and never enumerating others' data or invoking tools directly.
