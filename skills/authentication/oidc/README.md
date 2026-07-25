# OIDC Authentication Skill

**File:** `skills/authentication/oidc/README.md`

**Version:** 1.0.0

---

# Purpose

The OIDC Authentication Skill is an Authentication-tier domain skill that evaluates
how an in-scope application implements the OpenID Connect identity layer atop OAuth2
within the Robust PenTest Platform (RPP).

It examines ID token validation, nonce usage, discovery-document and JWKS exposure,
UserInfo handling, and identity-claim validation, reporting weaknesses such as
unvalidated ID token signatures, missing nonce, absent audience or issuer checks,
and insecure identity-claim handling.

The skill consumes the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) produced by Discovery. It drives the
[HTTP Client](../../shared/http-client/README.md) and SHALL NOT issue requests
directly. Every target-facing action is authorized by the
[Policy Engine](../../shared/policy-engine/README.md). It builds on the OAuth2
authorization behavior evaluated by the
[OAuth2 Authentication](../oauth2/README.md) skill.

---

# Goals

The OIDC Authentication Skill SHALL

- Evaluate ID token validation, nonce usage, and identity-claim validation
- Evaluate discovery-document, JWKS, and UserInfo handling
- Consume `web-application`, `endpoint`, and `api` Assets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every
  target-facing action
- Record [Observations](../../../schemas/observation.md) and promote them to
  [Evidence](../../../schemas/evidence.md)
- Emit [Findings](../../../schemas/finding.md) with
  [Risk](../../../schemas/risk.md) for OIDC weaknesses
- Remain tool independent

---

# Non-Goals

The OIDC Authentication Skill SHALL NOT

- Perform HTTP input or output directly
- Discover applications or endpoints (that is Discovery)
- Re-evaluate OAuth2 authorization-flow specifics (that is the OAuth2 skill)
- Validate JWT structure and signatures in depth (that is the JWT skill)
- Test authorization decisions of protected resources (that is the Authorization
  tier)
- Exploit weaknesses beyond the evidence required to confirm them
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client; discovery belongs to the Discovery
tier; authorization-flow, token-format, and authorization testing belong to
dedicated skills.

---

# Design Principles

The OIDC Authentication Skill SHALL be

- Scope-confined and policy-gated
- Evidence-backed for every Finding
- Deterministic given the same provider behavior
- Conservative — it confirms weaknesses without disruptive exploitation
- Credential-safe — it never persists ID tokens or secrets in evidence
- Tool independent

---

# Architecture

```
Authentication Agent

↓

OIDC Authentication Skill

├── Policy Gate            → Policy Engine
├── Discovery Prober      → HTTP Client
├── ID Token Analyzer
├── Nonce And Claim Analyzer
├── UserInfo Analyzer
├── Weakness Analyzer
├── Evidence Recorder     → Evidence
└── Finding Emitter

↓

Observations · Evidence · Findings · Risk
```

The skill orchestrates the HTTP Client to observe OIDC behavior. It SHALL remain
unaware of any transport implementation.

---

# Responsibilities

The OIDC Authentication Skill is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each
  target-facing action
- Observing discovery, ID token, and UserInfo behavior through the
  [HTTP Client](../../shared/http-client/README.md)
- Analyzing ID token validation, nonce usage, and identity-claim validation
- Detecting missing signature validation, missing nonce, and weak claim checks
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

Observe Discovery, ID Token, And UserInfo (HTTP Client)

↓

Analyze ID Token, Nonce, And Claims

↓

Record Observations → Evidence

↓

Analyze For OIDC Weaknesses

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

client_credentials_ref:

scope_id:

roe_id:
```

`target` SHALL be an in-scope OpenID Provider or relying-party application base URL.

`assets` reference the `web-application`, `endpoint`, and `api`
[Assets](../../../schemas/asset.md) under test.

`client_credentials_ref` MAY reference managed test client credentials. It SHALL be
a reference, never inline secrets.

`scope_id` and `roe_id` reference the assessment
[Scope](../../../schemas/scope.md) and
[Rules of Engagement](../../../schemas/rules-of-engagement.md).

---

# Produced Assets

The skill primarily consumes Assets. Where it confirms a distinct authenticated
identity context, it MAY record an `identity`
[Asset](../../../schemas/asset.md) with provenance. It SHALL NOT invent other Asset
types and SHALL NOT persist ID tokens or secrets on any Asset.

---

# Produced Findings

The skill MAY produce [Findings](../../../schemas/finding.md), each with
[Risk](../../../schemas/risk.md), for weaknesses such as

- ID token signatures not validated by the relying party
- Missing or unvalidated `nonce`, permitting replay
- Absent audience or issuer validation on ID tokens
- Discovery document or JWKS exposing unexpected or insecure configuration
- UserInfo endpoint served over cleartext or without proper authorization
- Identity claims trusted without verification

Every Finding SHALL reference supporting [Evidence](../../../schemas/evidence.md)
with ID tokens and secrets redacted.

---

# Policy Enforcement

The OIDC Authentication Skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every target-facing
action. Flow testing is an `active` action; it SHALL proceed only on an `allow`
decision and within the attached rate ceiling. Where a decision is
`requires_approval`, the skill SHALL defer the action until approval is granted.
Out-of-scope targets SHALL never be tested.

---

# Dependencies

The OIDC Authentication Skill depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Asset Schema](../../../schemas/asset.md)
- [Observation Schema](../../../schemas/observation.md)
- [Finding Schema](../../../schemas/finding.md)
- [Risk Schema](../../../schemas/risk.md)

The OIDC Authentication Skill SHALL NOT depend on other domain skills. It builds
conceptually on the OAuth2 skill's output but SHALL NOT take a package dependency on
it.

---

# Consumers

Typical consumers include

- The Authentication Agent and authentication workflows
- API Security skills that rely on identity context
- Reporting, through the produced Findings and Risk

---

# Outputs

Typical outputs MAY include

- Findings with Risk for OIDC weaknesses
- Observations and Evidence references
- Optional `identity` Assets for confirmed authenticated contexts

Outputs SHALL remain implementation independent.

---

# Security Principles

The OIDC Authentication Skill SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Confirm weaknesses without disruptive exploitation
- Redact ID tokens and secrets in all evidence
- Produce no Finding without supporting Evidence
- Reference managed credentials, never inline secrets
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope `web-application` Assets and managed client credentials
- Rely on the skill for OIDC identity-layer evaluation rather than ad hoc checks
- Treat produced Findings as inputs to remediation and reporting
- Capture the produced Evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue HTTP requests directly
- Bypass the Policy Engine
- Provide inline client secrets
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
- adr/ADR-001-oidc-authentication-skill.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [OAuth2 Authentication](../oauth2/README.md)
- [JWT Authentication](../jwt/README.md)

---

# Canonical Schemas

- [Asset](../../../schemas/asset.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Finding](../../../schemas/finding.md)
- [Risk](../../../schemas/risk.md)

---

# Architecture Decisions

- [ADR-001 — OIDC Authentication Skill](adr/ADR-001-oidc-authentication-skill.md)

---

# Future Extensions

Future versions MAY support

- Front-channel and back-channel logout evaluation
- Pairwise-subject and claim-source evaluation
- Federation and provider-metadata trust evaluation
- Handoff of identity context to API Security testing

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant OIDC Authentication Skill produces evidence-backed Findings for OpenID
Connect identity-layer weaknesses while acting strictly within scope and Rules of
Engagement through the Policy Engine, never persisting ID tokens or secrets, and
never invoking tools directly.
