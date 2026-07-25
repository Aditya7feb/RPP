# SAML Authentication Skill

**File:** `skills/authentication/saml/README.md`

**Version:** 1.0.0

---

# Purpose

The SAML Authentication Skill is an Authentication-tier domain skill that evaluates
how an in-scope service provider implements SAML-based single sign-on within the
Robust PenTest Platform (RPP).

It examines assertion signing and signature validation, audience and recipient
restrictions, replay protection, and binding security, reporting weaknesses such as
signature stripping, XML signature wrapping, acceptance of unsigned assertions, and
absent audience or recipient validation.

The skill consumes the `web-application`, `endpoint`, and `identity`
[Assets](../../../schemas/asset.md) produced by Discovery and prior Authentication
skills. It drives the [HTTP Client](../../shared/http-client/README.md) and SHALL
NOT issue requests directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md).

---

# Goals

The SAML Authentication Skill SHALL

- Evaluate assertion signing, signature validation, and canonicalization handling
- Evaluate audience, recipient, and replay protections and binding security
- Consume `web-application`, `endpoint`, and `identity` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for SAML weaknesses
- Remain tool independent

---

# Non-Goals

The SAML Authentication Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Evaluate OAuth2 or OIDC flows (those are dedicated skills)
- Test authorization decisions of protected resources (that is the Authorization
  tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; other federation protocols and authorization testing belong to dedicated
skills.

---

# Design Principles

The SAML Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same service-provider behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists assertions or secrets in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

SAML Authentication Skill

├── Policy Gate            → Policy Engine
├── Assertion Prober      → HTTP Client
├── Signature Analyzer
├── Restriction Analyzer
├── Replay Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe SAML behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The SAML Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing SAML assertion consumption through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing signature validation, canonicalization, and restriction enforcement
- Detecting signature stripping, signature wrapping, and replay
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

Observe Assertion Consumption (HTTP Client)

↓

Analyze Signature, Restrictions, And Replay

↓

Record Observations → Evidence

↓

Analyze For SAML Weaknesses

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

assertion_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope SAML service provider assertion-consumer endpoint.

`assets` reference the `web-application`, `endpoint`, and `identity`
[Assets](../../../schemas/asset.md) under test.

`assertion_ref` MAY reference a managed test assertion and signing material. It
SHALL be a reference, never inline assertion or key material.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. Where it confirms a distinct authenticated
identity context, it MAY record an `identity`
[Asset](../../../schemas/asset.md) with provenance. It SHALL NOT invent other Asset
types and SHALL NOT persist assertions or signing secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- Unsigned assertions accepted by the service provider
- Signature stripping accepted, where a removed signature is not detected
- XML signature wrapping accepted, where a wrapped element bypasses validation
- Audience restriction not enforced
- Recipient or destination not validated
- Assertion replay accepted due to absent identifier or timestamp validation
- Assertions transmitted over cleartext transport

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with assertions and signing material redacted.

---

# Policy Enforcement

The SAML Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Assertion testing is an `active` action; it SHALL proceed only on an
`allow` decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The SAML Authentication Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The SAML Authentication Skill SHALL NOT depend on other domain skills.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- Web Security and API skills that rely on federated identity context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for SAML weaknesses
- Observations and Evidence references
- Optional `identity` Assets for confirmed authenticated contexts

Outputs SHALL remain implementation independent.

---

# Security Principles

The SAML Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact assertions and signing material in all evidence
- Produce no Finding without supporting Evidence
- Reference managed assertions and keys, never inline material
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and a managed test assertion
- Rely on the skill for SAML evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline assertion or key material
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
- adr/ADR-001-saml-authentication-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [OIDC Authentication](../oidc/README.md)
- [Session Management](../sessions/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — SAML Authentication Skill](adr/ADR-001-saml-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- Identity-provider-initiated flow evaluation
- Metadata trust and certificate-rotation evaluation
- Single-logout evaluation
- Handoff of federated identity context to Web Security and API testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant SAML Authentication Skill produces evidence-backed Findings for SAML
single sign-on weaknesses while acting strictly within scope and Rules of Engagement
through the Policy Engine, never persisting assertions or signing material, and
never invoking tools directly.
